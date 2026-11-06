"""도장 서버가 모델에 실제로 보내는 글을 가로채 토큰 수를 세고 gpt-4o-mini 단가로 비용을 계산한다.
측정이 아니라 계산이다: 입력은 서버 코드가 만든 실제 글(tiktoken o200k_base 로 센 값, 메시지별 형식 토큰은 빼고 센 근사),
출력은 측정한 평균(또는 코드의 최대 토큰)을 쓴다. 외부 API 는 부르지 않는다(가짜 LLM)."""
import os, sys, json
sys.path.insert(0, r'C:/Users/Aiffel/Documents/github/routine-stamp-trial/server')
os.environ['LLM_PROVIDER'] = 'fake'
import tiktoken
from fastapi.testclient import TestClient
import main, llm as llm_module

enc = tiktoken.get_encoding('o200k_base')
tok = lambda s: len(enc.encode(s or ''))
IN, OUT = 0.15 / 1e6, 0.60 / 1e6

calls = []
class Capture(llm_module.FakeLLM):
    def complete_json(self, system, user, usage=None):
        calls.append(('json', system, user)); return super().complete_json(system, user, usage)
    def chat_stream(self, messages, usage=None):
        calls.append(('chat', None, messages)); return super().chat_stream(messages, usage)
    def complete_text(self, messages, max_tokens):
        calls.append(('text', None, messages)); return super().complete_text(messages, max_tokens)

cap = Capture()
main.app.dependency_overrides[main.get_llm] = lambda: cap
main.app.dependency_overrides[main.get_user_llm_factory] = lambda: (lambda key: cap)
client = TestClient(main.app)

def text_of(x):
    if isinstance(x, str): return x
    return '\n'.join((m.get('content') or '') if isinstance(m, dict) else str(m) for m in x)

def run_chat(history):
    calls.clear()
    r = client.post('/api/chat', json={'messages': history}, headers={'X-Forwarded-For': '198.51.100.%d' % (len(history) + 1)})
    ti = {}
    for kind, system, body in calls:
        t = tok(system or '') + tok(text_of(body))
        ti[kind] = ti.get(kind, 0) + t
    return r.status_code, ti

def mk(n):  # n번째 사용자 메시지까지의 대화(사용자·도우미 번갈아, 한 줄 60자쯤)
    h = []
    for i in range(n):
        h.append({'role': 'user', 'content': '오늘 물 마시기 루틴을 이어 가기가 어려웠어요. %d번째 이야기예요. 조금 더 편하게 하려면 어떻게 할까요?' % (i + 1)})
        if i < n - 1:
            h.append({'role': 'assistant', 'content': '물 마시기를 잊어버릴 때 보통 어떤 일이 생기나요? 작은 것부터 같이 정해 볼까요? %d' % (i + 1)})
    return h

out = {}
for n in (1, 5, 10, 20):
    code, ti = run_chat(mk(n))
    out[n] = (code, ti)
    print('대화', n, '번째 메시지', '상태', code, '| 입력 토큰 (모드 고르기 json / 답 쓰기 chat):', ti)

# 비용 계산: 출력은 측정 평균(모드 고르기 14, 답 쓰기 59), 상한은 코드의 최대 토큰(120, 450)
def cost(ti, o_json, o_chat):
    return ti.get('json', 0) * IN + o_json * OUT + ti.get('chat', 0) * IN + o_chat * OUT
print()
for n, (code, ti) in out.items():
    c_avg = cost(ti, 14, 59); c_max = cost(ti, llm_module.PLAN_TOKENS, llm_module.REPLY_TOKENS)
    print('대화 %2d번째: 평균 출력 기준 $%.6f (%.2f원@1,344) | 최대 출력 기준 $%.6f' % (n, c_avg, c_avg * 1344, c_max))

# 도장 그림: 입력은 서버가 만든 글, 출력은 최대(SVG_TOKENS)를 상한으로
calls.clear()
r = client.post('/api/stamp', json={'name': '물 마시기'}, headers={'X-Forwarded-For': '198.51.100.250'})
tin = sum(tok(text_of(b)) for k, s, b in calls)
print('\n도장 그림 요청 상태', r.status_code, '| 입력 토큰', tin, '| 최대 출력 토큰', llm_module.SVG_TOKENS)
print('도장 그림 한 건 상한: $%.6f (%.2f원@1,344) — 출력이 최대치일 때' % (tin * IN + llm_module.SVG_TOKENS * OUT, (tin * IN + llm_module.SVG_TOKENS * OUT) * 1344))
print('도장 그림 한 건 입력만: $%.6f' % (tin * IN))
