# Langfuse 2일차(노드 11) 실습 기록 — 보고서 재료

서비스: 루틴 도장판(`routine-stamp-trial`). 도우미 = OpenAI gpt-4o-mini(운영과 같은 모델), 심사 = Claude Sonnet(예정).
Langfuse: us.cloud, 조직 tigermorning's Organization / My Project, environment=development.

## 시작 전 (노드 10 계측 정리, 2026-11-03)
- Langfuse 공식 스킬(langfuse/skills@298b316) 설치 → 계측을 모범 사례에 맞춤: 이름 check-safety / choose-mode / generate-reply / check-numbers, 검사 둘은 guardrail, 한 턴은 agent, generation 에 토큰 수.
- 진짜 gpt-4o-mini 한 턴: choose-mode 939/23 토큰 $0.00015465, generate-reply 2048/74 토큰 $0.0003516, 첫 글자 1.005초, 턴 3.252초. trace 3978390913f8cc6b94a308cd88199a9c
- 진짜 호출에서 드러난 버그: 모드 고르기 실패 때 단계를 두 번 닫음(SDK 경고 "Calling end() on an ended span") → 한 번만 닫게 고침, 시험 186 통과.
- 옛 조회 API GET /api/public/traces 는 2026-11-16 제거 예고 → /api/public/v2/observations(fields 를 줘야 io·usage 가 옴).

## 스텝 1 시작 질문
- (사용자 답 아직 없음)

## 스텝 2 — 트레이스 모으기와 오류 분석
- 평가 사례 23건 × 2회 = 트레이스 46개, 진짜 LLM 호출 78번. 이 실행에서만 원문 수집(LANGFUSE_CAPTURE_TEXT=on), 시험 문장이라 실제 사용자 대화 아님. 메타데이터 eval_case·eval_run.
- 코드 채점 실패 17 → 채점기 문제 4(위기 2: 수집 스크립트가 llm_calls 를 안 넘김 / 부정문 오탐 '의지가 약하다기보다는' / 부분 문자열 오탐 '불가능해요'→'가능해요') + 판정 애매 1(선택지 줄을 문장으로 셈) → 진짜 실패 12~13 + 무작위 6개 읽기에서 조용한 실패 1.
- 퀴즈 답 2번(도구 선택 단계의 기간). 이유: 처음 틀린 단계부터 고친다.

| 실패 유형 | 개수 | 판정 기준 문장 | 판정 방법 |
|---|---|---|---|
| ① 모드를 잘못 고름(choose-mode) | 6 | 방법을 직접 물으면 advise, 자기 고민이면 listen/advise, 연구·효과 수치 질문은 범위 밖이 아니라 advise/listen | 코드 |
| ② 듣기 모드인데 방법 제안(generate-reply) | 4 | listen 답에는 행동 제안·방법이 없고 공감과 열린 질문만 | LLM 심사 |
| ③ 되묻기 되풀이(generate-reply) | 2(+1) | 직전 도우미 말이 질문이면 이번 답은 질문으로 끝나지 않는다 | 코드(judge.py 에 있음) |
| ④ 한 답에 질문 여러 개(조용한 실패) | 1 | 듣기 모드 답의 질문은 하나 | 코드 |

- 근거 없는 숫자 '5분'은 ①② 뒤에 따라 나오고 check-numbers 가 잡지만, 답을 다 보낸 뒤라 사용자는 이미 봄 → 코드로 고칠 후보.
- 메모 17개를 Langfuse 트레이스 댓글로 남김("[노드11 스텝2 오류 분석]" 머리말), 목록 API 로 17개 확인.
- 원자료: `_drafts/langfuse-day2-traces-run1.json`
