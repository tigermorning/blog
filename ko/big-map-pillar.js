// big-map.html 첫 화면(에이전트 설계 다섯 기둥)의 데이터.
// 기둥 = Anthropic CCA(Claude Certified Architect – Foundations) 시험의 다섯 영역. 번호·비중은 시험 안내서 그대로.
// 각 기둥의 items는 "그 영역이 묻는 것" 하나에 그 질문에 답하는 이 블로그 글을 붙인 것. gap은 아직 글이 없는 부분.
window.BIGMAP_PILLAR = {
 "title": "AI 에이전트 설계 — 다섯 기둥",
 "lead": "Anthropic이 2026년 3월에 낸 첫 공식 인증 시험 CCA(Claude Certified Architect)는 에이전트를 만드는 일을 다섯 영역으로 나누고, 영역마다 비중을 매겨요. 이 블로그의 글도 대부분 이 다섯 영역 가운데 하나를 받치고 있어요. 상자를 누르면 그 영역이 묻는 것과, 거기에 답하는 글이 읽을 순서대로 나와요.",
 "anatomy": "모델은 한 번 불리면 받은 입력 뒤에 글자를 이어 쓸 뿐이에요. 도구를 직접 실행하지도, 지난 대화를 기억하지도 못해요. 그래서 모델을 부르는 코드가 정할 게 넷이에요. 무엇을 시키고 어떤 모양으로 답받을지(④), 어떤 도구를 쥐여 줄지(②), 무엇을 보여 줄지(⑤), 그리고 그 호출을 몇 번·어떤 순서로 엮을지(①). 이 넷을 정한 코드까지 합친 것이 에이전트예요. Claude Code(③)는 이 넷을 이미 갖춘 완성품이라, 우리는 설정 파일로 내 프로젝트에 맞춰 써요.",
 "nodes": [
  { "id": "brain", "region": "brain", "label": "토대 · 머신러닝·LLM", "sub": "모델 한 번 호출이 실제로 하는 일 — 토큰을 읽고 다음 토큰을 계산", "chips": ["토큰", "컨텍스트 창", "트랜스포머"] },
  { "id": "web", "region": "web", "label": "토대 · 웹 서비스", "sub": "에이전트가 돌아갈 서버, API 키를 숨길 자리, 기록을 남길 DB", "chips": ["API", "백엔드", "프록시"] },
  { "id": "p4", "pillar": "p4" },
  { "id": "p2", "pillar": "p2" },
  { "id": "p5", "pillar": "p5" },
  { "id": "p1", "pillar": "p1" },
  { "id": "p3", "pillar": "p3" }
 ],
 "edges": [
  ["brain", "p4", "무엇을 시키나"],
  ["brain", "p2", "무엇을 쥐여 주나"],
  ["brain", "p5", "무엇을 보여 주나"],
  ["p4", "p1", "호출 한 번"],
  ["p2", "p1", "호출 한 번"],
  ["p5", "p1", "호출 한 번"],
  ["web", "p1", "돌아갈 자리"],
  ["p1", "p3", "완성품을 설정으로"]
 ],
 "pillars": [
  {
   "id": "p1",
   "num": "1",
   "name": "에이전트 아키텍처와 오케스트레이션",
   "weight": "27%",
   "color": "var(--folder-7)",
   "sub": "모델 호출 여러 번을 순서·갈림길·반복으로 엮고, 필요하면 여러 에이전트에게 나누는 설계",
   "chips": ["stop_reason 루프", "다섯 패턴", "서브에이전트", "상태·종료 조건"],
   "question": "모델 호출을 몇 번, 어떤 순서로 엮어야 일 하나가 끝까지 가나?",
   "scene": "고객 문의에 답하는 에이전트가 응답을 받자마자 화면에 띄웠더니, 가끔 문장 중간에서 끊긴 답이 나가요. 또 한 에이전트에 일을 몰았더니 느리고 자주 헤매요. 이 영역은 응답이 왔을 때 다음에 무엇을 할지, 일을 어디서 나눌지를 물어요.",
   "items": [
    { "ask": "루프 — 응답이 왔다고 답이 끝난 게 아니다", "plain": "응답에 함께 오는 stop_reason(모델이 멈춘 이유)을 보고 도구 실행·끝내기·잘린 답 버리기를 가르는 반복 구조예요.", "posts": ["what-is-ai-agent.html", "agent-react-loop-and-autogpt.html", "langgraph-branches-and-tool-loop.html", "cca-exam-agent-anti-patterns.html"] },
    { "ask": "워크플로냐 에이전트냐", "plain": "순서가 정해진 일은 코드가 순서를 정하고, 정할 수 없는 일만 모델에게 다음 단계를 고르게 해요.", "posts": ["what-is-automation-workflow-agent.html", "langgraph-what-and-why.html", "langgraph-state-node-edge.html"] },
    { "ask": "일을 쪼개는 다섯 모양", "plain": "순서대로 잇기·분류해 한 갈래로·동시에 돌려 합치기·LLM이 몇 갈래일지 정하기·통과할 때까지 고쳐 쓰기.", "posts": ["langgraph-pattern-chaining.html", "langgraph-pattern-routing.html", "langgraph-pattern-parallelization.html", "langgraph-pattern-orchestrator-worker.html", "langgraph-pattern-evaluator-optimizer.html"] },
    { "ask": "코디네이터와 서브에이전트 — 나눌지, 무엇을 넘길지", "plain": "나누면 조율 비용이 생겨요. 나눌 때는 하위 에이전트에게 꼭 필요한 맥락만 넘기고, 돌아올 때는 요약만 받아요.", "posts": ["multi-agent-split-gains-and-losses.html", "multi-agent-four-structures.html", "multi-agent-three-runs-abc.html"] },
    { "ask": "상태·승인·종료 조건", "plain": "지금 어디까지 했는지(상태), 사람이 거절하면 어떻게 되는지(승인), 언제 멈추는지(종료 조건)를 코드로 적어 둬요.", "posts": ["my-harness-flow-and-state.html", "langgraph-branch-drills.html"] },
    { "ask": "꼭 지킬 순서는 프롬프트가 아니라 코드로", "plain": "\"환불 전에 본인 확인부터\"처럼 어기면 사고가 나는 순서는 프롬프트로 부탁하지 말고 코드 검사로 막아요.", "posts": ["cs-agent-grounding.html"], "gap": "Claude Code·Agent SDK의 훅(도구 실행 직전·직후에 끼어드는 코드)과, 중단한 세션 이어 가기·갈라 가기" }
   ]
  },
  {
   "id": "p2",
   "num": "2",
   "name": "도구 설계와 MCP 연동",
   "weight": "18%",
   "color": "var(--folder-2)",
   "sub": "모델이 도구를 헷갈리지 않고 고르고, 실패했을 때 다음 수를 알게 하는 도구 정의",
   "chips": ["도구 설명·스키마", "도구 배분", "MCP 서버", "최소 권한"],
   "question": "모델이 맞는 도구를 고르고, 도구가 실패해도 다음에 할 일을 알게 하려면?",
   "scene": "재고를 물었는데 에이전트가 이름이 비슷한 주문 조회 도구를 불러요. 도구가 에러를 내자 같은 호출을 끝없이 되풀이해요. 이 영역은 도구 이름·설명·입력 모양·에러 응답을 어떻게 적어야 모델이 덜 헷갈리는지를 물어요.",
   "items": [
    { "ask": "모델은 도구를 실행하지 않는다", "plain": "모델은 \"이 도구를 이 값으로 불러 달라\"는 요청만 돌려주고, 실제 실행은 모델을 부른 내 코드(하네스)가 해요.", "posts": ["agent-tool-design-and-harness.html", "mcp-skill-tool-call-anatomy.html"] },
    { "ask": "설명과 스키마가 선택을 정한다", "plain": "모델은 도구 이름·설명·입력 스키마만 보고 고르니, 비슷한 도구끼리는 언제 쓰고 언제 안 쓰는지까지 적어요.", "posts": ["tool-contract-and-schema.html", "my-harness-interfaces.html"] },
    { "ask": "도구를 에이전트마다 나눠 쥐여 주기", "plain": "한 에이전트에 도구를 몰면 고르기가 흔들려요. 4~5개를 넘기 시작하면 에이전트를 나누거나 필요할 때만 도구를 불러오게 해요.", "posts": ["cca-exam-agent-anti-patterns.html", "mcp-skill-context-and-search.html"] },
    { "ask": "MCP 서버 연결", "plain": "MCP는 도구를 한 번 만들어 여러 AI 앱에 꽂아 쓰게 하는 연결 규격이에요. 서버를 만들고 호스트에 등록해 첫 호출까지 확인해요.", "posts": ["mcp-usb-c-for-ai.html", "mcp-skill-protocol-roles.html", "mcp-skill-building-server.html", "mcp-skill-host-connection.html"] },
    { "ask": "권한은 최소로", "plain": "읽기만 필요한 도구에 쓰기 권한을 주지 않고, 되돌릴 수 없는 도구는 사람 승인을 거치게 해요.", "posts": ["tool-permission-and-evaluation.html", "openclaw-security-boundaries.html"], "gap": "도구 에러를 \"다시 해도 되는 실패인지\" 같은 칸으로 구조화해 돌려주는 법, 모델에게 특정 도구를 강제로 쓰게 하는 설정(tool_choice)" }
   ]
  },
  {
   "id": "p3",
   "num": "3",
   "name": "Claude Code 설정과 워크플로",
   "weight": "20%",
   "color": "var(--folder-8)",
   "sub": "완성된 코딩 에이전트를 내 프로젝트 규칙대로, 사람이 지켜보지 않아도 돌게 하는 설정",
   "chips": ["CLAUDE.md 계층", "스킬·명령", "권한", "CI에서 -p"],
   "question": "이미 만들어진 코딩 에이전트를 내 프로젝트 규칙대로, 자동 실행에서도 멈추지 않게 쓰려면?",
   "scene": "팀 규칙을 전부 CLAUDE.md 한 파일에 넣었더니 상관없는 폴더 작업에서 규칙끼리 부딪혀요. 매일 밤 도는 자동 실행에 Claude Code를 넣었더니 권한을 묻는 자리에서 멈춰요. 이 영역은 규칙·스킬·권한을 어디에 두고, 자동 실행에서는 어떻게 부르는지를 물어요.",
   "items": [
    { "ask": "설치하고 첫 작업 맡기기", "plain": "터미널에서 Claude Code를 띄우고, 요청→확인→수정 반복으로 파일 하나를 끝까지 만들어 봐요.", "posts": ["ai-agent-dev-environment.html", "my-first-web-project.html", "vibe-coding-loop.html"] },
    { "ask": "규칙 파일은 층으로", "plain": "홈 폴더·프로젝트·하위 폴더의 CLAUDE.md가 합쳐져 읽히고, 부딪히면 가장 구체적인 파일이 이겨요.", "posts": ["ai-skills-and-rules-files.html", "agents-md-and-cache-economics.html", "cca-exam-agent-anti-patterns.html"] },
    { "ask": "반복 작업은 스킬·명령·플러그인으로", "plain": "매번 설명하던 절차를 SKILL.md나 슬래시 명령으로 남겨 두면 필요할 때만 불러와 써요.", "posts": ["mcp-skill-why-skill-needed.html", "mcp-skill-writing-skill-md.html", "claude-plugins-and-spec-driven-development.html"] },
    { "ask": "권한과 되돌릴 수 있는 실행", "plain": "파일을 지우거나 옮기는 일은 먼저 미리보기(dry-run)로 보고, 에이전트가 물어보지 않고 할 수 있는 범위를 정해요.", "posts": ["ai-folder-cleanup.html", "ai-permissions-local-models-and-token-cost.html"] },
    { "ask": "자동 실행(CI/CD)에서는 대화하듯 부르지 않기", "plain": "파이프라인에서는 claude -p처럼 질문 하나에 답하고 끝나는 모드로 부르고, 필요한 권한은 미리 허락해 둬요.", "posts": ["learning-git-5.html", "newsletter-agent-publish-schedule.html", "cca-exam-agent-anti-patterns.html"], "gap": "계획 모드(바로 고치지 않고 먼저 계획만 세우게 하기)와 바로 실행을 언제 고르는지, 폴더·파일 경로마다 다른 규칙을 거는 법" }
   ]
  },
  {
   "id": "p4",
   "num": "4",
   "name": "프롬프트 엔지니어링과 구조화된 출력",
   "weight": "20%",
   "color": "var(--folder-5)",
   "sub": "모델 답을 사람이 아니라 다음 코드가 그대로 읽을 수 있게 받는 지시와 출력 형식",
   "chips": ["명확한 기준", "예시(few-shot)", "JSON 스키마", "검증 후 재시도"],
   "question": "모델 답을 다음 단계 코드가 그대로 읽을 수 있게, 매번 같은 모양으로 받으려면?",
   "scene": "계약서에서 날짜·금액을 뽑아 표에 넣으려는데, 모델이 어떤 날은 문장으로, 어떤 날은 표로 답해요. 가끔 원문에 없는 금액도 채워 넣어요. 이 영역은 기준을 어떻게 적고, 출력 모양을 어떻게 고정하고, 틀린 답을 어떻게 걸러 다시 받는지를 물어요.",
   "items": [
    { "ask": "\"알아서 잘\" 대신 판단 기준", "plain": "\"중요한 것만\"이 아니라 무엇이 중요한지, 언제 보고하지 말아야 하는지를 구체적으로 적어요.", "posts": ["what-is-prompt-engineering.html", "instruction-design-basics.html", "instruction-failure-types.html", "instruction-design-principles.html"] },
    { "ask": "애매한 경우는 예시로 보여 주기", "plain": "말로 설명하기 어려운 경계 사례는 입력-정답 예시 몇 개(few-shot)로 보여 줘요. 효과는 내 과제에서 직접 재 봐야 해요.", "posts": ["prompt-engineering-history.html", "prompt-technique-verification.html", "eleven-ways-same-question.html"] },
    { "ask": "출력 모양을 스키마로 고정", "plain": "답을 JSON 스키마에 맞춰 받게 하면 다음 코드가 문장을 해석하지 않고 칸에서 값을 꺼내요.", "posts": ["output-format-and-metrics.html", "langgraph-pattern-routing.html"] },
    { "ask": "검사하고, 틀리면 이유를 붙여 다시", "plain": "받은 답을 원문·규칙과 대조해 틀리면 무엇이 틀렸는지 알려 주며 다시 요청해요. 원문에 없는 값은 재시도로 안 생겨요.", "posts": ["newsletter-agent-summarize-verify.html", "langgraph-pattern-evaluator-optimizer.html", "rag-chatbot-llm-judge.html"] },
    { "ask": "문서에서 구조화된 값 뽑기", "plain": "뽑을 칸(스키마)이 곧 답할 수 있는 질문을 정해요. 이름 표기를 하나로 맞추는 정규화도 이 단계 일이에요.", "posts": ["graphrag-build-knowledge-graph.html", "cs-agent-improve.html"], "gap": "급하지 않은 대량 요청을 모아 싸게 맡기는 배치 API의 실제 사용법(개념만 에이전트 안티패턴 글에 있어요)" }
   ]
  },
  {
   "id": "p5",
   "num": "5",
   "name": "컨텍스트 관리와 신뢰성",
   "weight": "15%",
   "color": "var(--folder-6)",
   "sub": "대화가 길어지고 단계가 늘어도 사실을 잃지 않고, 모를 때는 사람에게 넘기는 설계",
   "chips": ["컨텍스트 창", "압축·떼어 내기", "사람에게 넘기기", "근거·출처"],
   "question": "대화가 길어지고 단계가 늘어도 사실을 잃지 않고, 모를 땐 멈추게 하려면?",
   "scene": "상담이 길어지자 에이전트가 앞에서 고객이 말한 주문 번호를 잊어요. 확신이 없는데도 그럴듯한 답을 내고, 앞 단계가 틀린 값을 넘기면 뒤 단계가 그대로 믿어요. 이 영역은 무엇을 기억에 남기고, 언제 사람에게 넘기고, 오류가 어디서 번지는지를 물어요.",
   "items": [
    { "ask": "컨텍스트 창은 유한하다", "plain": "모델이 한 번에 읽는 입력에는 한도가 있고, 넣은 만큼 돈이 들어요.", "posts": ["what-is-ai-token.html", "tokens-and-context-window-cost.html", "context-window-budget.html"] },
    { "ask": "길게 넣어도 안 읽힐 수 있다", "plain": "긴 입력의 가운데는 잘 안 읽히고, 대화가 길어질수록 앞의 사실이 흐려져요.", "posts": ["lost-in-the-middle-and-context-rot.html"] },
    { "ask": "고르고, 떼어 내고, 압축하기", "plain": "필요한 조각만 찾아 넣고(RAG), 긴 로그는 따로 읽혀 요약만 받고, 대화가 커지면 앞부분을 요약으로 줄여요.", "posts": ["context-strategy-and-rag.html", "harness-action-format-and-context.html", "context-experiment-and-injection-defense.html"] },
    { "ask": "모를 때는 사람에게 넘기기", "plain": "모델이 매긴 확신도가 기준 아래면 억지로 고르지 않고 사람에게 넘기는 자리를 설계에 넣어요.", "posts": ["cs-agent-routing-eval.html", "cs-agent-grounding.html"] },
    { "ask": "오류는 다음 단계로 번진다", "plain": "앞 단계가 틀린 값을 넘기면 뒤 단계는 그걸 사실로 믿어요. 단계마다 검사하고, 결과와 과정을 함께 채점해요.", "posts": ["ocr-assembly-line-and-error-propagation.html", "multi-agent-judging-records.html", "harness-evaluation-and-comparison.html"] },
    { "ask": "근거를 보여 주는 답", "plain": "답마다 어느 문서의 어느 조각에서 왔는지 남기면, 사람이 검토할 때 틀린 답을 빨리 찾아요.", "posts": ["rag-chatbot-project-overview.html", "graphrag-goldenset-eval.html"] }
   ]
  }
 ],
 "scenarios": [
  { "name": "고객 지원 해결 에이전트", "posts": ["cs-agent-routing-eval.html"], "note": "CS 상담 에이전트 만들기 (17~19편)", "pillars": ["p1", "p2", "p5"] },
  { "name": "Claude Code로 코드 생성", "posts": ["ai-agent-dev-environment.html"], "note": "AI 코딩 환경 세팅 시리즈", "pillars": ["p3"] },
  { "name": "멀티 에이전트 리서치 시스템", "posts": ["langgraph-pattern-orchestrator-worker.html", "multi-agent-split-gains-and-losses.html"], "note": "오케스트레이터-워커 · 멀티 에이전트 실험", "pillars": ["p1", "p5"] },
  { "name": "개발 생산성 도구", "posts": ["mcp-skill-tool-call-anatomy.html"], "note": "MCP와 Skill로 업무 맡기기 시리즈", "pillars": ["p2", "p3"] },
  { "name": "CI/CD 안의 Claude Code", "posts": ["learning-git-5.html", "newsletter-agent-publish-schedule.html"], "note": "GitHub Actions 예약 실행", "pillars": ["p3"] },
  { "name": "구조화된 데이터 추출", "posts": ["newsletter-agent-summarize-verify.html", "graphrag-build-knowledge-graph.html"], "note": "요약 세 칸 · 지식 그래프 삼중항 추출", "pillars": ["p4", "p5"] }
 ],
 "titles": {
  "cca-exam-agent-anti-patterns.html": "에이전트 안티패턴 다섯 가지"
 }
};
