// 공부 사다리 데이터 — 손으로 쓴다. 칸 사이 관계는 연결된 글의 문장에 근거한 것만 쓴다.
// flow: 칸({f,title,tag}) · 이음({to:'next'|'add', label}) · 갈래({choose, options:[{when, steps:[칸, 이음, 칸…]}]})
//   next = 같은 일을 이어서 하거나 이어서 읽는다 / add = 앞 것은 그대로 두고 더한다 / 갈래 = 상황에 맞게 하나를 고른다(순서 없음)
window.LADDERS = [
  { mark: '①', name: 'AI 답을 바로잡기', flow: [
    { f: 'what-is-prompt-engineering', title: '어디가 문제인지 찾기', tag: '프롬프트 엔지니어링' },
    { to: 'next', label: '한 가지만 바꿔 보기' },
    { choose: '무엇이 부족했나', options: [
      { when: '지시가 애매했다면', steps: [{ f: 'instruction-design-basics', title: '지시를 네 부품으로', tag: '지시 설계' }] },
      { when: 'AI가 자료를 못 봤다면', steps: [{ f: 'context-strategy-and-rag', title: '넣을 자료 정하기', tag: 'RAG' }] }
    ] }
  ] },
  { mark: '②', name: 'AI를 내 컴퓨터에서 돌리기', flow: [
    { f: 'quantization-why-it-still-works', title: '모델 크기 줄이기', tag: '양자화' },
    { to: 'next', label: '줄인 크기로' },
    { f: 'kv-cache-and-vram-budget', title: '메모리에 들어갈지 계산', tag: 'KV 캐시·VRAM' },
    { to: 'next', label: '들어가면' },
    { f: 'running-local-llm-with-ollama', title: '직접 돌려 보기', tag: 'Ollama' },
    { to: 'next', label: '돌려 본 뒤' },
    { f: 'three-ways-to-run-an-llm', title: '어디서 돌릴지 고르기', tag: '로컬·API·섞어 쓰기' }
  ] },
  { mark: '③', name: 'AI에게 일 맡기기', flow: [
    { f: 'what-is-ai-agent', title: '챗봇·워크플로·에이전트 구분', tag: 'AI 에이전트' },
    { to: 'next', label: '맡길 일을 보고' },
    { choose: '무엇이 필요한가', options: [
      { when: '같은 설명을 매번 되풀이하면', steps: [{ f: 'ai-skills-and-rules-files', title: '설명을 파일로 남기기', tag: '스킬·규칙 파일' }] },
      { when: 'AI가 손댈 수단이 필요하면', steps: [
        { f: 'agent-tool-design-and-harness', title: '도구 쥐여 주기', tag: '도구 설계' },
        { to: 'add', label: '같은 규격으로 연결' },
        { f: 'mcp-usb-c-for-ai', title: '도구를 규격으로 잇기', tag: 'MCP' }
      ] },
      { when: '여러 단계를 이어야 하면', steps: [
        { f: 'langgraph-what-and-why', title: '단순한 흐름부터', tag: '워크플로' },
        { to: 'add', label: '꼭 필요할 때만' },
        { f: 'multi-agent-four-structures', title: '구조 고르기', tag: '멀티 에이전트' }
      ] }
    ] }
  ] },
  { mark: '④', name: '일의 순서(워크플로) 짜기', flow: [
    { choose: '일이 어떤 모양인가', options: [
      { when: '정해진 순서로 다 거치면', steps: [{ f: 'langgraph-pattern-chaining', title: '순서대로 잇기', tag: '프롬프트 체이닝' }] },
      { when: '여러 갈래 중 하나만 가면', steps: [{ f: 'langgraph-pattern-routing', title: '하나만 고르기', tag: '라우팅' }] },
      { when: '개수를 아는 일을 한꺼번에', steps: [{ f: 'langgraph-pattern-parallelization', title: '동시에 돌리기', tag: '병렬화' }] },
      { when: '몇 개로 나눌지 미리 모르면', steps: [{ f: 'langgraph-pattern-orchestrator-worker', title: '나누기를 맡기기', tag: '오케스트레이터-워커' }] },
      { when: '결과를 보고 고쳐 써야 하면', steps: [{ f: 'langgraph-pattern-evaluator-optimizer', title: '되돌려 고치기', tag: '평가자-최적화자' }] }
    ] }
  ] },
  { mark: '⑤', name: '하네스 살펴보고 직접 만들기', flow: [
    { f: 'harness-observation-and-feature-map', title: '남의 하네스 보는 법', tag: '화면 관찰' },
    { to: 'next', label: '보는 법을 익힌 뒤' },
    { f: 'my-harness-users-and-prd', title: '내 하네스 설계', tag: 'PRD부터' },
    { to: 'next', label: '만든 뒤' },
    { f: 'my-harness-benchmark-local-port', title: '남이 정한 채점으로 재기', tag: '벤치마크' }
  ] },
  { mark: '⑥', name: 'AI에게 이미지 읽히기', flow: [
    { choose: '무엇을 알고 싶은가', options: [
      { when: '글자', steps: [{ f: 'why-cant-ai-read-this-pdf', title: '글자 읽기', tag: 'OCR' }] },
      { when: '무엇이 어디에 있나', steps: [{ f: 'object-detection-and-iou', title: '박스로 찾기', tag: '객체 탐지' }] },
      { when: '정확한 경계', steps: [{ f: 'segmentation-and-sam', title: '경계로 자르기', tag: '분할·SAM' }] },
      { when: '설명·질문 답하기', steps: [{ f: 'vision-language-models', title: '말로 묻고 답 듣기', tag: 'VLM' }] }
    ] }
  ] },
  { mark: '⑦', name: '소리를 글로, 글을 소리로', flow: [
    { choose: '어느 방향인가', options: [
      { when: '소리 → 글자', steps: [
        { f: 'speech-to-text-history', title: '받아쓰기 원리', tag: 'STT' },
        { to: 'next', label: '내 컴퓨터에서' },
        { f: 'choosing-a-local-whisper', title: '받아쓰기 모델 고르기', tag: 'Whisper' }
      ] },
      { when: '글자 → 소리', steps: [
        { f: 'choosing-a-voice-synthesis-tool', title: '음성 합성 도구 고르기', tag: 'TTS' },
        { to: 'add', label: '실제 목소리를 흉내 내려면' },
        { f: 'voice-cloning-and-responsible-ai', title: '해도 되는지 따지기', tag: '음성 복제 윤리' }
      ] }
    ] }
  ] },
  { mark: '⑧', name: '사진으로 3D 공간 만들기', flow: [
    { f: 'birth-of-nerf-and-gaussian-splatting', title: '장면을 3D로 담는 방법', tag: 'NeRF·스플래팅' },
    { to: 'next', label: '그전에 거리부터' },
    { f: 'recovering-depth-from-photos', title: '사진에서 거리 되찾기', tag: '깊이 추정' },
    { to: 'next', label: '얻은 점을' },
    { f: 'turning-points-into-splats', title: '알갱이로 바꾸기', tag: '스플랫 변환' },
    { to: 'next', label: '파일이 크면' },
    { f: 'shrinking-splat-files-for-the-web', title: '웹에 올릴 크기로', tag: '파일 최적화' }
  ] },
  { mark: '⑨', name: 'AI로 그림 만들기', flow: [
    { f: 'gan-to-diffusion-models', title: '그림을 만드는 원리', tag: '확산모델' },
    { to: 'add', label: '압축해서 가볍게' },
    { f: 'latent-diffusion-and-distillation', title: '가볍게 만드는 법', tag: '잠재확산·증류' },
    { to: 'next', label: '직접 만들 때' },
    { choose: '몇 장을 만드나', options: [
      { when: '몇 장이면', steps: [{ f: 'choosing-image-generation-tools', title: '도구 고르기', tag: '브라우저·코드·무료 GPU' }] },
      { when: '수백 장이면', steps: [{ f: 'automating-image-generation', title: '코드로 만들기', tag: '자동화' }] }
    ] }
  ] },
  { mark: '⑩', name: '과학 데이터에 AI 쓰기', flow: [
    { choose: '어떤 데이터인가', options: [
      { when: '표', steps: [{ f: 'foundation-models-for-tables', title: '표 읽기', tag: '표 파운데이션 모델' }] },
      { when: '단백질 서열', steps: [
        { f: 'from-sequence-to-structure', title: '서열로 모양 맞히기', tag: '구조 예측' },
        { to: 'add', label: '거꾸로, 모양에서 서열을' },
        { f: 'designing-proteins-backwards', title: '없던 단백질 설계', tag: '단백질 역설계' }
      ] },
      { when: '원자와 분자', steps: [{ f: 'graphs-and-interatomic-forces', title: '원자 사이 힘 계산', tag: '그래프 신경망' }] }
    ] }
  ] },
  { mark: '⑪', name: '만든 서비스 내보내기', flow: [
    { f: 'cloud-run-source-deploy-meaning', title: '손으로 배포', tag: 'Cloud Run 소스 배포' },
    { to: 'add', label: '같은 순서를 자동으로' },
    { f: 'github-actions-auto-deploy', title: '머지하면 자동 배포', tag: 'GitHub Actions' },
    { to: 'add', label: '소스 대신 이미지로' },
    { f: 'build-once-promote-image', title: '한 번 만든 이미지 그대로', tag: '이미지 승격' },
    { to: 'add', label: '바뀌는 동안 끊기지 않게' },
    { f: 'cloud-run-zero-downtime-deploy', title: '끊김 없이 바꾸기', tag: '무중단 배포' }
  ] }
];
