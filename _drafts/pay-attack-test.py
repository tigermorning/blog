"""도장 서버(가짜 LLM, 내 컴퓨터)에만 시험한다. 외부 API는 부르지 않는다."""
import subprocess, sys, time, json, os, threading
import httpx
from concurrent.futures import ThreadPoolExecutor

SERVER_DIR = r"C:\Users\Aiffel\Documents\github\routine-stamp-trial\server"
PORT = 8123
URL = f"http://127.0.0.1:{PORT}"
BODY = {"messages": [{"role": "user", "content": "물 마시기 칸을 만들었는데 자꾸 까먹어요."}]}


def start():
    env = {k: v for k, v in os.environ.items() if not k.startswith(("LANGFUSE", "LLM_", "OPENAI", "ANTHROPIC"))}
    env["LLM_PROVIDER"] = "fake"
    p = subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--port", str(PORT), "--log-level", "warning"],
                         cwd=SERVER_DIR, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(60):
        try:
            if httpx.get(URL + "/health", timeout=1).status_code == 200:
                return p
        except Exception:
            time.sleep(0.3)
    p.kill(); raise SystemExit("server did not start")


def fire(n, headers_fn, path="/api/chat", body=BODY, workers=None):
    def one(i):
        try:
            r = httpx.post(URL + path, json=body, headers=headers_fn(i), timeout=30)
            return r.status_code
        except Exception as e:
            return type(e).__name__
    with ThreadPoolExecutor(workers or n) as ex:
        res = list(ex.map(one, range(n)))
    out = {}
    for s in res:
        out[s] = out.get(s, 0) + 1
    return out


results = {}
tests = [
    ("A. 같은 주소에서 동시에 10건", lambda: fire(10, lambda i: {})),
    ("B. 같은 주소에서 동시에 30건", lambda: fire(30, lambda i: {}, workers=30)),
    ("C. 주소 표시(X-Forwarded-For)를 요청마다 바꿔 130건", lambda: fire(130, lambda i: {"X-Forwarded-For": f"10.0.{i // 250}.{i % 250}"}, workers=20)),
    ("D. 도장 그림(/api/stamp) 같은 주소 10건", lambda: fire(10, lambda i: {}, path="/api/stamp", body={"name": "물 마시기"}, workers=10)),
    ("E. 도장 그림 주소 표시를 바꿔 50건", lambda: fire(50, lambda i: {"X-Forwarded-For": f"10.1.0.{i}"}, path="/api/stamp", body={"name": "물 마시기"}, workers=10)),
]
for name, fn in tests:
    p = start()
    try:
        results[name] = fn()
    finally:
        p.kill(); p.wait()
        time.sleep(0.5)
    print(name, results[name], flush=True)
json.dump(results, open(os.path.join(os.path.dirname(__file__), "attack-results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
