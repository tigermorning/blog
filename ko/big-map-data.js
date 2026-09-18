// big-map.html의 데이터. 글 목록(posts.html)과 각 글 본문에서 뽑아 만들었다.
window.BIGMAP = {
 "regions": [
  {
   "id": "web",
   "name": "웹 서비스",
   "color": "var(--folder-1)",
   "role": "사용자가 만나는 화면, 그 뒤에서 요청을 받는 서버, 기록을 쌓는 데이터베이스.",
   "scenario": "친구에게 보낸 링크가 안 열리던 데서 시작해요. 화면은 목업 데이터로 먼저 완성하고, API 키는 프록시 서버 뒤에 숨기고, 회원 정보는 SQL 표에 담아 무료 플랫폼에 배포해요.",
   "subs": [
    "web-frontend",
    "backend-deploy",
    "database"
   ],
   "edges": [
    [
     "web-frontend",
     "backend-deploy",
     "요청"
    ],
    [
     "backend-deploy",
     "database",
     "읽고 쓰기"
    ]
   ]
  },
  {
   "id": "agent",
   "name": "오케스트레이션(에이전트 흐름 설계)",
   "color": "var(--folder-7)",
   "role": "모델 호출 여러 번을 순서·갈림길·반복으로 엮어 일 하나를 끝까지 해내게 하는 틀.",
   "scenario": "같은 뼈대(State·Node·Edge)와 다섯 패턴으로 뉴스레터 에이전트, CS 상담 에이전트, GraphRAG 추천 에이전트를 만들었어요. CS 에이전트는 실패 사례를 하나씩 고쳐 정확도를 59%에서 94%로 올렸어요.",
   "subs": [
    "langgraph-basics",
    "langgraph-patterns",
    "newsletter-agent-project",
    "cs-agent-project",
    "graphrag-project",
    "multi-agent-lab",
    "harness-observe",
    "harness-build",
    "openclaw",
    "paper-notes"
   ],
   "edges": [
    [
     "langgraph-basics",
     "langgraph-patterns",
     "조합"
    ],
    [
     "langgraph-patterns",
     "newsletter-agent-project",
     "적용"
    ],
    [
     "langgraph-patterns",
     "cs-agent-project",
     "적용"
    ],
    [
     "cs-agent-project",
     "graphrag-project",
     "검색 확장"
    ],
    [
     "langgraph-patterns",
     "multi-agent-lab",
     "여럿으로"
    ],
    [
     "multi-agent-lab",
     "harness-observe",
     "틀을 보기"
    ],
    [
     "paper-notes",
     "harness-observe",
     "행동 형식"
    ],
    [
     "harness-observe",
     "harness-build",
     "직접 짜기"
    ],
    [
     "harness-observe",
     "openclaw",
     "완성품 운영"
    ]
   ]
  },
  {
   "id": "talk",
   "name": "프롬프트·컨텍스트 엔지니어링",
   "color": "var(--folder-5)",
   "role": "모델에게 무엇을 시키고(지시), 무엇을 보여 주고(맥락), 무엇을 쥐여 줄지(도구) 정하는 설계.",
   "scenario": "고객 문의 챗봇에 같은 질문을 두고 지시를 A·B·C안으로 바꿔 채점하고, 정책 문서·대화 이력 중 무엇을 컨텍스트에 실을지 고르고, 재고 조회 도구는 스키마로 입력을 제한해요.",
   "subs": [
    "prompt-agent-concepts",
    "instruction-design",
    "context-engineering",
    "agent-tools",
    "tool-design"
   ],
   "edges": [
    [
     "prompt-agent-concepts",
     "instruction-design",
     "지시 설계"
    ],
    [
     "prompt-agent-concepts",
     "context-engineering",
     "맥락 설계"
    ],
    [
     "prompt-agent-concepts",
     "agent-tools",
     "도구 쥐기"
    ],
    [
     "agent-tools",
     "tool-design",
     "도구 설계"
    ]
   ]
  },
  {
   "id": "brain",
   "name": "머신러닝·LLM",
   "color": "var(--folder-3)",
   "role": "데이터에서 규칙을 배우고, 다음 토큰을 계산해 답을 만드는 부분.",
   "scenario": "코딩 에이전트가 짠 MNIST 분류기를 검증하고, 긴 문서 중간이 뭉개지는 이유를 어텐션 구조로 설명하고, 민감한 계약서는 로컬 Ollama로·나머지는 API로 보내는 결정을 내려요.",
   "subs": [
    "ml-basics",
    "llm-theory",
    "local-llm"
   ],
   "edges": [
    [
     "ml-basics",
     "llm-theory",
     "키우면"
    ],
    [
     "llm-theory",
     "local-llm",
     "내 PC로"
    ]
   ]
  },
  {
   "id": "senses",
   "name": "멀티모달",
   "color": "var(--folder-4)",
   "role": "글자 밖의 입력·출력 — 사진·문서·소리·그림·공간·분자를 다루는 모델들.",
   "scenario": "계약서 스캔본에서 금액을 표로 뽑고(OCR), 발표 표지 이미지를 프롬프트로 만들고, 녹음을 로컬 Whisper로 받아 적고, 폰 영상으로 3D 스캔을 만들어요.",
   "subs": [
    "vision-ocr",
    "multimodal-voice",
    "image-video-gen",
    "three-d-reconstruction",
    "science-ai"
   ],
   "edges": [
    [
     "vision-ocr",
     "multimodal-voice",
     "언어와 합침"
    ],
    [
     "multimodal-voice",
     "image-video-gen",
     "글로 그림"
    ],
    [
     "vision-ocr",
     "three-d-reconstruction",
     "사진→공간"
    ],
    [
     "three-d-reconstruction",
     "science-ai",
     "자연으로"
    ]
   ]
  },
  {
   "id": "tools",
   "name": "RAG·MCP·자동화",
   "color": "var(--folder-2)",
   "role": "모델이 내 문서·내 업무에 손을 뻗게 해 주는, 직접 만든 연결 장치.",
   "scenario": "n8n으로 반복 문의 처리를 그림처럼 그려 보고, 근거 문서를 함께 보여 주는 RAG 챗봇을 GitHub Pages에 올리고, 팀 업무 기록을 읽는 MCP 서버와 판정 기준을 담은 SKILL.md로 주간보고서를 써요.",
   "subs": [
    "automation-n8n",
    "chatbot-project",
    "mcp-skill-series"
   ],
   "edges": []
  },
  {
   "id": "bench",
   "name": "개발 환경·Git",
   "color": "var(--folder-8)",
   "role": "위의 모든 것을 만들고 고치고 저장하고 세상에 내보내는 곳.",
   "scenario": "Git을 모르던 상태에서 Claude Code로 첫 웹페이지를 만들고, 결과를 커밋으로 남겨 GitHub Pages에 올렸어요. 이 블로그가 그 결과물이에요. 버그에서 얻은 교훈은 규칙 파일에 적어 다음 작업이 그 위에 쌓이게 해요.",
   "subs": [
    "work-with-ai",
    "ai-coding-setup",
    "coding-agent-tools",
    "git-github"
   ],
   "edges": [
    [
     "work-with-ai",
     "ai-coding-setup",
     "뭘 만들지"
    ],
    [
     "ai-coding-setup",
     "coding-agent-tools",
     "도구 고르기"
    ],
    [
     "ai-coding-setup",
     "git-github",
     "저장"
    ],
    [
     "coding-agent-tools",
     "git-github",
     "커밋·배포"
    ]
   ]
  }
 ],
 "world": {
  "title": "질문 하나가 AI 서비스를 지나가는 길",
  "lead": "상담 챗봇에 누군가 \"환불 되나요?\"라고 적었다고 해 볼게요. 답이 돌아오기까지 이 블로그의 글 거의 전부가 어딘가에서 일해요. 번호를 따라가 보고, 궁금한 상자를 눌러 들어가세요.",
  "nodes": [
   {
    "id": "user",
    "label": "사용자",
    "sub": "질문을 적는 사람"
   },
   {
    "id": "bench",
    "label": "개발 환경·Git",
    "sub": "이 모든 걸 만들고 고쳐서 내보내는 곳"
   },
   {
    "id": "web",
    "label": "웹 서비스",
    "sub": "화면·서버·데이터베이스",
    "step": "1"
   },
   {
    "id": "agent",
    "label": "오케스트레이션(에이전트 흐름 설계)",
    "sub": "일의 순서와 갈림길을 정하는 틀",
    "step": "2"
   },
   {
    "id": "talk",
    "label": "프롬프트·컨텍스트 엔지니어링",
    "sub": "지시·맥락·도구를 한 입력으로",
    "step": "3"
   },
   {
    "id": "senses",
    "label": "멀티모달",
    "sub": "사진·문서·소리·공간을 다루는 모델"
   },
   {
    "id": "brain",
    "label": "머신러닝·LLM",
    "sub": "입력을 읽고 다음 토큰을 계산",
    "step": "4"
   },
   {
    "id": "tools",
    "label": "RAG·MCP·자동화",
    "sub": "모델이 내 문서·업무에 닿게 하는 연결",
    "step": "5"
   }
  ],
  "edges": [
   [
    "user",
    "web",
    "질문"
   ],
   [
    "bench",
    "web",
    "만들어 배포"
   ],
   [
    "web",
    "agent",
    "넘김"
   ],
   [
    "agent",
    "talk",
    "조립"
   ],
   [
    "talk",
    "brain",
    "호출"
   ],
   [
    "senses",
    "brain",
    "글자 밖 입력"
   ],
   [
    "brain",
    "tools",
    "도구 요청"
   ]
  ],
  "steps": [
   [
    "① 웹 서비스",
    "화면이 질문을 서버로 보내요. 모델 API 키는 브라우저가 아니라 서버가 쥐고, 대화 기록은 데이터베이스에 남아요."
   ],
   [
    "② 오케스트레이션",
    "이 질문이 환불·배송 같은 몇 갈래 중 어디인지 먼저 고르고, 어떤 순서로 처리할지 정해요."
   ],
   [
    "③ 프롬프트·컨텍스트 엔지니어링",
    "지시문, 매뉴얼에서 찾아 온 관련 조각(RAG), 쓸 수 있는 도구 목록을 모델이 읽을 입력 하나로 조립해요."
   ],
   [
    "④ 머신러닝·LLM",
    "모델이 입력을 읽고 답을 쓰거나, \"환불 규정을 조회해 달라\"고 도구 호출을 요청해요."
   ],
   [
    "⑤ RAG·MCP·자동화",
    "도구가 매뉴얼·데이터에서 실제 값을 가져와 다시 모델에게 넣어 줘요. 모델이 기간·금액을 지어내지 않게 하는 장치예요."
   ],
   [
    "돌아가는 길",
    "완성된 답은 검사(심사·지표)를 거쳐 ②→①을 거꾸로 타고 화면으로 가요."
   ],
   [
    "곁가지",
    "질문이 사진·음성이면 멀티모달 모델이 먼저 글자로 바꿔 넣어요. 이 전부는 개발 환경에서 코딩 에이전트와 Git으로 만들어 배포해요."
   ]
  ]
 },
 "threads": [
  {
   "id": "eval",
   "name": "평가",
   "color": "var(--hit-ink)",
   "question": "맞혔다는 말을 어떻게 숫자로 바꾸나",
   "lead": "만든 것마다 마지막엔 같은 질문이 남아요. 정말 나아졌나? 분류기의 혼동 행렬에서 시작해 에이전트 벤치마크까지, 같은 생각이 점점 큰 대상으로 옮겨 가요.",
   "posts": [
    "confusion-matrix-and-metrics.html",
    "output-format-and-metrics.html",
    "prompt-technique-verification.html",
    "eleven-ways-same-question.html",
    "rag-chatbot-llm-judge.html",
    "rag-chatbot-prompt-experiment.html",
    "cs-agent-improve.html",
    "graphrag-goldenset-eval.html",
    "tool-permission-and-evaluation.html",
    "multi-agent-judging-records.html",
    "harness-evaluation-and-comparison.html",
    "my-harness-scoring-and-report.html"
   ]
  },
  {
   "id": "guard",
   "name": "보안·권한",
   "color": "var(--miss-ink)",
   "question": "키·데이터·권한이 새지 않게",
   "lead": "SSH 키 한 쌍에서 시작해 에이전트 권한 모드까지, 대상은 달라도 질문은 같아요. 누가 무엇을 할 수 있게 둘 것인가.",
   "posts": [
    "ssh-concept.html",
    "ai-code-security-basics.html",
    "sql-injection-and-backup-basics.html",
    "what-is-proxy-server.html",
    "what-is-cors.html",
    "where-does-your-data-stay.html",
    "ai-permissions-local-models-and-token-cost.html",
    "context-experiment-and-injection-defense.html",
    "tool-permission-and-evaluation.html",
    "harness-minimal-and-permission.html",
    "openclaw-security-boundaries.html",
    "voice-cloning-and-responsible-ai.html"
   ]
  },
  {
   "id": "cost",
   "name": "비용·자원",
   "color": "var(--folder-6)",
   "question": "같은 일을 더 싸고 가볍게",
   "lead": "토큰 하나의 값에서 시작해 컨텍스트 예산, 캐시, 내 노트북 메모리, 로컬과 API의 손익분기까지. 모두 한정된 자원을 어디에 쓸지의 문제예요.",
   "posts": [
    "what-is-ai-token.html",
    "tokens-and-context-window-cost.html",
    "context-window-budget.html",
    "agents-md-and-cache-economics.html",
    "mcp-skill-context-and-search.html",
    "training-vs-inference-memory.html",
    "quantization-why-it-still-works.html",
    "kv-cache-and-vram-budget.html",
    "cost-and-control-of-local-llm.html",
    "openclaw-session-records-and-usage.html"
   ]
  }
 ],
 "subs": {
  "git-github": {
   "sub": "git-github",
   "role": "블로그를 코드로 만들고 자동 공개·발행하는 실전 기반",
   "scenario": "Git이 뭔지 모르던 상태에서 Claude와 대화하며 하루 만에 Git 설치, GitHub 연결, GitHub Pages 홈페이지, GitHub Actions 예약 발행까지 만든 실제 과정이다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "로컬 Git 준비",
      "posts": [
       "learning-git-1.html",
       "git-commit-concept.html"
      ]
     },
     {
      "id": "n2",
      "label": "GitHub 연결",
      "posts": [
       "learning-git-2.html",
       "ssh-concept.html"
      ]
     },
     {
      "id": "n3",
      "label": "코드 주고받기",
      "posts": [
       "learning-git-3.html"
      ]
     },
     {
      "id": "n4",
      "label": "웹으로 배포",
      "posts": [
       "learning-git-4.html"
      ]
     },
     {
      "id": "n5",
      "label": "자동 발행",
      "posts": [
       "learning-git-5.html"
      ]
     },
     {
      "id": "n6",
      "label": "브랜치 실험",
      "posts": [
       "learning-git-6.html"
      ]
     },
     {
      "id": "n7",
      "label": "검색 노출",
      "posts": [
       "blog-seo-basics.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "등록하다"
     ],
     [
      "n2",
      "n3",
      "복제하다"
     ],
     [
      "n3",
      "n4",
      "공개하다"
     ],
     [
      "n4",
      "n5",
      "예약하다"
     ],
     [
      "n3",
      "n6",
      "실험하다"
     ],
     [
      "n4",
      "n7",
      "노출되다"
     ]
    ]
   },
   "posts": [
    {
     "file": "learning-git-1.html",
     "concept": "Git 설치와 초기 설정",
     "one_line": "저장은 덮어쓰기, 커밋은 시점을 사진처럼 남기는 것",
     "practice": "새 컴퓨터를 세팅할 때 git config로 이름·이메일부터 등록한다",
     "analogy": "도장 파기와 서류철 열기",
     "keywords": [
      "Git",
      "커밋",
      "저장소",
      "터미널",
      "바이브코딩"
     ],
     "links": [
      "git-commit-concept.html",
      "what-is-vibe-coding.html",
      "learning-git-2.html"
     ]
    },
    {
     "file": "learning-git-2.html",
     "concept": "SSH로 GitHub 연결",
     "one_line": "SSH는 비밀번호 대신 열쇠 한 쌍으로 나를 증명하는 방식",
     "practice": "매번 비밀번호 없이 GitHub에 push할 때 SSH 키로 인증한다",
     "analogy": "도장 원본 안 넘기고 자국만 보여주기",
     "keywords": [
      "SSH",
      "공개키",
      "개인키",
      "GitHub 계정"
     ],
     "links": [
      "ssh-concept.html",
      "learning-git-1.html",
      "learning-git-3.html"
     ]
    },
    {
     "file": "learning-git-3.html",
     "concept": "커밋하고 푸시하기",
     "one_line": "저장소를 내려받아 고치고 기록해 다시 올려보내는 기본 동작",
     "practice": "고친 파일을 인터넷에 반영할 때 add·commit·push 세 단계를 거친다",
     "analogy": "",
     "keywords": [
      "clone",
      "commit",
      "push",
      "origin/main"
     ],
     "links": [
      "learning-git-2.html",
      "learning-git-4.html",
      "git-commit-concept.html"
     ]
    },
    {
     "file": "learning-git-4.html",
     "concept": "GitHub Pages",
     "one_line": "저장소에 index.html만 올리면 무료로 진짜 웹주소가 생긴다",
     "practice": "포트폴리오를 인터넷 주소로 공개할 때 저장소 이름을 아이디.github.io로 짓는다",
     "analogy": "손님을 맞는 주인, 호스팅",
     "keywords": [
      "GitHub Pages",
      "index.html",
      "호스팅",
      "404"
     ],
     "links": [
      "learning-git-3.html",
      "learning-git-5.html",
      "what-is-browser-cache.html"
     ]
    },
    {
     "file": "learning-git-5.html",
     "concept": "GitHub Actions",
     "one_line": "정해진 시각마다 GitHub 서버가 큐의 글을 하루 3개씩 대신 올린다",
     "practice": "글을 몰아 써두고 매일 자동으로 올리고 싶을 때 cron과 큐 파일로 예약한다",
     "analogy": "매표소 줄서기 같은 큐",
     "keywords": [
      "GitHub Actions",
      "cron",
      "큐",
      "워크플로"
     ],
     "links": [
      "learning-git-4.html",
      "learning-git-6.html",
      "blog-seo-basics.html"
     ]
    },
    {
     "file": "learning-git-6.html",
     "concept": "브랜치와 병합",
     "one_line": "main은 그대로 두고 가지에서 실험한 뒤 괜찮으면 합친다",
     "practice": "이미 잘 돌아가는 자동화를 고칠 때 브랜치에서 먼저 실험하고 병합한다",
     "analogy": "나뭇가지처럼 갈라졌다 합쳐지는 구조",
     "keywords": [
      "브랜치",
      "병합",
      "checkout",
      "merge"
     ],
     "links": [
      "learning-git-5.html",
      "git-commit-concept.html"
     ]
    },
    {
     "file": "git-commit-concept.html",
     "concept": "커밋과 저장의 차이",
     "one_line": "저장은 슬롯 하나를 덮어쓰고, 커밋은 슬롯을 계속 새로 쌓는 것",
     "practice": "예전 상태로 되돌아가고 싶을 때 저장 대신 커밋으로 슬롯을 만들어둔다",
     "analogy": "게임 세이브 슬롯",
     "keywords": [
      "커밋",
      "저장",
      "git config",
      "repository"
     ],
     "links": [
      "learning-git-1.html",
      "learning-git-3.html"
     ]
    },
    {
     "file": "ssh-concept.html",
     "concept": "SSH 공개키·개인키 원리",
     "one_line": "개인키는 안 보내고 그 자리에서 만든 서명만 서버에 보여준다",
     "practice": "GitHub이 비밀번호 없이 나를 알아볼 때 챌린지-리스폰스로 서명을 검증한다",
     "analogy": "인감도장 원본과 등록된 자국",
     "keywords": [
      "SSH",
      "챌린지-리스폰스",
      "공개키",
      "패스키"
     ],
     "links": [
      "learning-git-2.html",
      "git-commit-concept.html"
     ]
    },
    {
     "file": "blog-seo-basics.html",
     "concept": "검색 노출(SEO) 기초",
     "one_line": "구글은 크롤러가 미리 만든 색인에서 답을 꺼내 보여줄 뿐이다",
     "practice": "직접 만든 HTML 사이트를 검색에 걸리게 할 때 sitemap과 meta description을 챙긴다",
     "analogy": "도서관 사서의 카드 목록",
     "keywords": [
      "SEO",
      "크롤러",
      "sitemap.xml",
      "meta description",
      "Open Graph"
     ],
     "links": [
      "learning-git-4.html",
      "learning-git-5.html"
     ]
    }
   ],
   "name": "Git·GitHub 입문"
  },
  "ai-coding-setup": {
   "sub": "ai-coding-setup",
   "role": "AI에게 코드를 맡기고 결과를 검증하는 실전 작업 습관",
   "scenario": "Git도 모르던 상태에서 Node.js·npm·터미널을 설치하고, Claude Code에게 첫 웹페이지와 폴더 정리를 맡긴 뒤 dry-run으로 검토·승인하며 바이브 코딩 루프를 완성한 과정이다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "개념 이해",
      "posts": [
       "what-is-vibe-coding.html",
       "what-is-ai-token.html",
       "what-is-browser-cache.html",
       "what-is-github-contribution-graph.html"
      ]
     },
     {
      "id": "n2",
      "label": "작업대 세팅",
      "posts": [
       "ai-agent-dev-environment.html",
       "ai-agent-dev-environment-check.html"
      ]
     },
     {
      "id": "n3",
      "label": "첫 결과물 만들기",
      "posts": [
       "my-first-web-project.html",
       "vibe-coding-loop.html"
      ]
     },
     {
      "id": "n4",
      "label": "터미널 다루기",
      "posts": [
       "terminal-shell-kernel-prompt.html",
       "terminal-practice.html"
      ]
     },
     {
      "id": "n5",
      "label": "맡기고 검증",
      "posts": [
       "ai-folder-cleanup.html",
       "terminal-vs-ai-retrospective.html"
      ]
     },
     {
      "id": "n6",
      "label": "실무 적용",
      "posts": [
       "translation-review-automation-idea.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "세팅하다"
     ],
     [
      "n2",
      "n3",
      "만들다"
     ],
     [
      "n3",
      "n4",
      "이해하다"
     ],
     [
      "n4",
      "n5",
      "맡기다"
     ],
     [
      "n5",
      "n6",
      "적용하다"
     ]
    ]
   },
   "posts": [
    {
     "file": "what-is-vibe-coding.html",
     "concept": "바이브 코딩",
     "one_line": "말로 시키면 AI가 코드를 짜고 실행, 사람은 결과만 판단",
     "practice": "결과가 느낌엔 좋은데 틀렸을까 의심될 때 구조화·검증·기술감각으로 확인한다",
     "analogy": "셰프에게 말로 주문하기",
     "keywords": [
      "바이브코딩",
      "no-code",
      "루프",
      "검증"
     ],
     "links": [
      "learning-git-1.html",
      "ai-agent-dev-environment.html",
      "what-is-ai-token.html"
     ]
    },
    {
     "file": "what-is-ai-token.html",
     "concept": "AI 토큰",
     "one_line": "토큰은 AI가 글을 세는 최소 단위이자 요금 단위",
     "practice": "대화가 길어져 AI가 느려지고 조건을 잊을 때 새 대화로 나눠 토큰을 아낀다",
     "analogy": "버스 토큰처럼 낱개로 세어지는 값",
     "keywords": [
      "토큰",
      "컨텍스트 창",
      "API 비용",
      "무한 루프"
     ],
     "links": [
      "what-is-vibe-coding.html",
      "what-is-browser-cache.html"
     ]
    },
    {
     "file": "what-is-browser-cache.html",
     "concept": "브라우저 캐시",
     "one_line": "브라우저가 속도를 위해 내 컴퓨터에 묻어둔 옛 페이지 복사본",
     "practice": "사이트를 고쳐 올렸는데 화면이 그대로일 때 강력 새로고침·시크릿창·다른 기기 순으로 확인한다",
     "analogy": "탐험가가 길목에 묻어둔 보급품",
     "keywords": [
      "캐시",
      "강력 새로고침",
      "시크릿 창",
      "GitHub Pages"
     ],
     "links": [
      "learning-git-4.html",
      "what-is-ai-token.html"
     ]
    },
    {
     "file": "what-is-github-contribution-graph.html",
     "concept": "GitHub 잔디",
     "one_line": "1년치 날짜 칸에 그날 활동 기록이 있으면 초록으로 칠하는 그래프",
     "practice": "며칠째 회색 칸이 이어질 때 실제로 손을 놓았던 시기를 확인한다",
     "analogy": "출석 도장판",
     "keywords": [
      "Contribution graph",
      "커밋",
      "비공개 저장소",
      "빈 커밋"
     ],
     "links": [
      "git-commit-concept.html",
      "what-is-browser-cache.html",
      "ai-agent-dev-environment.html"
     ]
    },
    {
     "file": "ai-agent-dev-environment.html",
     "concept": "개발 환경 세팅",
     "one_line": "AI가 내 컴퓨터에서 일하려면 Node.js·npm·uv·Git·터미널이 필요",
     "practice": "AI에게 홈페이지를 만들어 달라기 전 다섯 도구로 작업대부터 차린다",
     "analogy": "요리사 혼자로는 못 하는 주방 차리기",
     "keywords": [
      "Node.js",
      "npm",
      "uv",
      "PATH",
      "CLI"
     ],
     "links": [
      "what-is-vibe-coding.html",
      "ai-agent-dev-environment-check.html",
      "learning-git-1.html"
     ]
    },
    {
     "file": "ai-agent-dev-environment-check.html",
     "concept": "설치 확인과 오류 전달법",
     "one_line": "npm은 준비할 때만, Node.js는 서버가 켜진 내내 실행된다",
     "practice": "설치됐다는 AI 말을 그대로 안 믿고 터미널에서 버전 숫자를 직접 확인한다",
     "analogy": "",
     "keywords": [
      "npm install",
      "node --version",
      "curl",
      "nvm"
     ],
     "links": [
      "ai-agent-dev-environment.html",
      "my-first-web-project.html"
     ]
    },
    {
     "file": "my-first-web-project.html",
     "concept": "첫 HTML 웹페이지",
     "one_line": "HTML은 텍스트 파일이라 브라우저·메모장 두 가지로 직접 검토된다",
     "practice": "AI가 만든 첫 파일을 받을 때 제목·본문·화면 세 가지를 스스로 검토한다",
     "analogy": "식당의 홀·주방·냉장고",
     "keywords": [
      "HTML",
      "pwd",
      "New-Item",
      "프론트엔드"
     ],
     "links": [
      "ai-agent-dev-environment-check.html",
      "vibe-coding-loop.html"
     ]
    },
    {
     "file": "vibe-coding-loop.html",
     "concept": "바이브 코딩 루프",
     "one_line": "지시→생성→판단→재지시를 반복해 결과를 다듬어가는 과정",
     "practice": "결과가 마음에 안 들 때 실패로 여기지 않고 추가할 것·지킬 것을 나눠 재지시한다",
     "analogy": "건물 골조(HTML)와 인테리어(CSS)",
     "keywords": [
      "루프",
      "CSS",
      "태그",
      "재지시"
     ],
     "links": [
      "my-first-web-project.html",
      "terminal-shell-kernel-prompt.html"
     ]
    },
    {
     "file": "terminal-shell-kernel-prompt.html",
     "concept": "터미널·셸·커널·프롬프트",
     "one_line": "터미널은 창, 셸은 통역사, 커널은 진짜 일꾼, 프롬프트는 대기 신호",
     "practice": "에러가 났을 때 이름을 못 찾으면 셸, 권한이 거부되면 커널 문제로 나눠 짚는다",
     "analogy": "달걀 껍데기(셸)와 알맹이(커널)",
     "keywords": [
      "셸",
      "커널",
      "PATH",
      "시스템 콜",
      "세션"
     ],
     "links": [
      "ai-agent-dev-environment-check.html",
      "terminal-practice.html"
     ]
    },
    {
     "file": "terminal-practice.html",
     "concept": "PowerShell 실습",
     "one_line": "pwd·ls·cd·mkdir·mv를 연습 폴더에서 손으로 반복해 익힌다",
     "practice": "파일을 옮기기 전에 pwd로 위치부터, 옮긴 뒤 ls로 결과부터 확인한다",
     "analogy": "",
     "keywords": [
      "pwd",
      "mv",
      "별명(alias)",
      "연습 폴더"
     ],
     "links": [
      "terminal-shell-kernel-prompt.html",
      "ai-folder-cleanup.html"
     ]
    },
    {
     "file": "ai-folder-cleanup.html",
     "concept": "dry-run 파일 정리",
     "one_line": "실제로 옮기지 않고 계획만 먼저 보여주는 것이 dry-run",
     "practice": "AI에게 되돌리기 어려운 파일 정리를 맡길 때 dry-run으로 승인 전에 검토한다",
     "analogy": "물 없이 동선만 맞추는 소방 훈련",
     "keywords": [
      "dry-run",
      "승인",
      "분류 기준",
      "삭제 금지"
     ],
     "links": [
      "terminal-practice.html",
      "terminal-vs-ai-retrospective.html"
     ]
    },
    {
     "file": "terminal-vs-ai-retrospective.html",
     "concept": "직접 vs AI 자동화",
     "one_line": "결과를 눈으로 확인할 수 있으면 맡기고, 아니면 직접 한다",
     "practice": "일을 맡길지 직접 할지 망설여질 때 결과를 눈으로 확인 가능한지로 정한다",
     "analogy": "",
     "keywords": [
      "판단 기준",
      "dry-run",
      "검증",
      "손으로 해본 경험"
     ],
     "links": [
      "ai-folder-cleanup.html",
      "translation-review-automation-idea.html"
     ]
    },
    {
     "file": "translation-review-automation-idea.html",
     "concept": "컴퓨팅 사고",
     "one_line": "감이 아니라 규칙 대조인 일부터 분해·패턴·추상화·알고리즘으로 자동화",
     "practice": "내 업무를 자동화할 때 감각이 필요한 일과 규칙 대조인 일을 먼저 가른다",
     "analogy": "",
     "keywords": [
      "컴퓨팅 사고",
      "분해",
      "API",
      "근거 기록"
     ],
     "links": [
      "what-is-vibe-coding.html",
      "terminal-vs-ai-retrospective.html"
     ]
    }
   ],
   "name": "AI 코딩 환경 세팅"
  },
  "multi-agent-lab": {
   "sub": "multi-agent-lab",
   "role": "여러 에이전트로 나눌지, 어떤 구조로 나눌지 실험으로 판정한다",
   "scenario": "같은 SWE-bench 버그 다섯 건을 기준선(A)·워크플로(B)·오케스트레이션(C) 세 방식으로 고치고, 테스트 통과와 행동 기록 두 층으로 채점해 채택·축소·폐기를 판정했다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "나눌지 판정",
      "posts": [
       "multi-agent-split-gains-and-losses.html"
      ]
     },
     {
      "id": "n2",
      "label": "구조 선택",
      "posts": [
       "multi-agent-four-structures.html"
      ]
     },
     {
      "id": "n3",
      "label": "세 방식 실행",
      "posts": [
       "multi-agent-three-runs-abc.html"
      ]
     },
     {
      "id": "n4",
      "label": "두 층 채점",
      "posts": [
       "multi-agent-judging-records.html"
      ]
     },
     {
      "id": "n5",
      "label": "도구로 문제 해결",
      "posts": [
       "multi-agent-ecosystem-tools.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "판정하면"
     ],
     [
      "n2",
      "n3",
      "구조 고르면"
     ],
     [
      "n3",
      "n4",
      "실행하면"
     ],
     [
      "n4",
      "n5",
      "문제 남으면"
     ]
    ]
   },
   "posts": [
    {
     "file": "multi-agent-split-gains-and-losses.html",
     "concept": "나눌지 판정표",
     "one_line": "나눈다는 건 컨텍스트와 책임을 다시 배치하는 일이다",
     "practice": "조사 과제를 여럿에게 나눌지 정할 때, 여섯 줄 판정표에 과업을 직접 대 본다",
     "analogy": "조사 프로젝트 팀(팀장·팀원)",
     "keywords": [
      "멀티 에이전트",
      "리드",
      "워커",
      "판정표"
     ],
     "links": [
      "multi-agent-four-structures.html"
     ]
    },
    {
     "file": "multi-agent-four-structures.html",
     "concept": "네 가지 연결 구조",
     "one_line": "구조는 누가 나누고 누가 다음 행동을 정하는지를 정한다",
     "practice": "자료 조사는 팬아웃·합성, 초안 검토는 비평-수정처럼 과업에 맞는 구조를 고른다",
     "analogy": "역할별 칸이 있는 작업 보드",
     "keywords": [
      "오케스트레이터-워커",
      "팬아웃·합성",
      "비평-수정",
      "인계"
     ],
     "links": [
      "multi-agent-split-gains-and-losses.html",
      "multi-agent-three-runs-abc.html"
     ]
    },
    {
     "file": "multi-agent-three-runs-abc.html",
     "concept": "A/B/C 세 실행 방식",
     "one_line": "같은 버그를 다음 행동을 누가 정하는지만 바꿔 세 번 실행한다",
     "practice": "멀티 에이전트가 낫다는 말을 검증할 때, 같은 문제를 A/B/C 세 방식으로 직접 돌려본다",
     "analogy": "오케스트라(고정 악보 vs 지휘자 판단)",
     "keywords": [
      "Claude Agent SDK",
      "턴 예산",
      "locator",
      "서브에이전트"
     ],
     "links": [
      "multi-agent-four-structures.html",
      "multi-agent-judging-records.html"
     ]
    },
    {
     "file": "multi-agent-judging-records.html",
     "concept": "두 층 채점",
     "one_line": "테스트 통과 여부와 행동 기록을 따로 판정해야 찍어 맞힌 성공을 가른다",
     "practice": "통과했다는 보고를 받으면, 결과 층과 행동 층을 나눠 인용 근거로 다시 확인한다",
     "analogy": "",
     "keywords": [
      "LLM judge",
      "evidence_quote",
      "채택·축소·폐기",
      "고정·조작·측정"
     ],
     "links": [
      "multi-agent-three-runs-abc.html",
      "multi-agent-ecosystem-tools.html"
     ]
    },
    {
     "file": "multi-agent-ecosystem-tools.html",
     "concept": "네 문제와 도구 지도",
     "one_line": "컨텍스트 단절·재현 불가·모델 고정·상태 불가시는 다른 도구가 겨냥한다",
     "practice": "새 도구를 붙이기 전에 그 도구가 조율·모델·관측 중 어느 층을 바꾸는지 먼저 판단한다",
     "analogy": "",
     "keywords": [
      "Agent Teams",
      "Workflows",
      "oh-my-claudecode",
      "herdr"
     ],
     "links": [
      "multi-agent-judging-records.html"
     ]
    }
   ],
   "name": "멀티 에이전트 실험"
  },
  "openclaw": {
   "sub": "openclaw",
   "role": "상시 대기하는 개인 에이전트 게이트웨이를 설치·보안·확장까지 운영한다",
   "scenario": "텔레그램으로 말을 걸면 답하고 정해진 시간에 자동화가 도는 개인 비서를 설치·인증·권한 설정·채널 연결·자동화 예약까지 실제로 구축했다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "설치·온보딩",
      "posts": [
       "openclaw-what-and-where-from.html",
       "openclaw-install-and-first-chat.html"
      ]
     },
     {
      "id": "n2",
      "label": "기록·사용량 확인",
      "posts": [
       "openclaw-session-records-and-usage.html"
      ]
     },
     {
      "id": "n3",
      "label": "채널 연결",
      "posts": [
       "openclaw-telegram-channel-and-pairing.html"
      ]
     },
     {
      "id": "n4",
      "label": "권한·보안 경계",
      "posts": [
       "openclaw-security-boundaries.html"
      ]
     },
     {
      "id": "n5",
      "label": "역할 분리",
      "posts": [
       "openclaw-multi-agent-bindings.html"
      ]
     },
     {
      "id": "n6",
      "label": "자동화 예약",
      "posts": [
       "openclaw-automations-scheduling.html"
      ]
     },
     {
      "id": "n7",
      "label": "코어·확장 선택",
      "posts": [
       "openclaw-pi-core-and-extensions.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "실행하면"
     ],
     [
      "n2",
      "n3",
      "확인 후"
     ],
     [
      "n3",
      "n4",
      "연결하면"
     ],
     [
      "n4",
      "n5",
      "권한 정하면"
     ],
     [
      "n5",
      "n6",
      "역할 나누면"
     ],
     [
      "n6",
      "n7",
      "예약 건 뒤"
     ]
    ]
   },
   "posts": [
    {
     "file": "openclaw-what-and-where-from.html",
     "concept": "게이트웨이 개념",
     "one_line": "부를 때만 오는 도구가 아니라 늘 대기하며 부탁을 받는 집사형 에이전트다",
     "practice": "이름이 바뀐 오류 메시지를 만나면, 지우기 전에 진단 명령으로 같은 도구의 흔적인지 확인한다",
     "analogy": "집에 상주하는 집사",
     "keywords": [
      "게이트웨이",
      "채널",
      "Clawdbot",
      "Moltbot"
     ],
     "links": [
      "openclaw-install-and-first-chat.html"
     ]
    },
    {
     "file": "openclaw-install-and-first-chat.html",
     "concept": "설치·온보딩·첫 대화",
     "one_line": "연습 폴더→npm 설치→온보딩→진단 두 개→WebChat 순서로 확인한다",
     "practice": "진단 명령의 경고를 중간까지 다 읽고, 경고가 있으면 채팅으로 넘어가지 않는다",
     "analogy": "새 직원의 첫 출근일",
     "keywords": [
      "onboard",
      "doctor",
      "인증 경로",
      "~/.openclaw"
     ],
     "links": [
      "openclaw-what-and-where-from.html",
      "openclaw-session-records-and-usage.html"
     ]
    },
    {
     "file": "openclaw-session-records-and-usage.html",
     "concept": "세션 기록과 사용량",
     "one_line": "말한 것과 한 것은 세션 기록에서 서로 다른 줄에 남는다",
     "practice": "파일 만들었다는 답을 받으면, 결과 줄이 실제로 있는지 확인한 뒤 다음 일을 맡긴다",
     "analogy": "병원의 진료 기록과 영수증",
     "keywords": [
      "toolCall",
      "toolResult",
      "/status",
      "/usage"
     ],
     "links": [
      "openclaw-install-and-first-chat.html",
      "openclaw-telegram-channel-and-pairing.html"
     ]
    },
    {
     "file": "openclaw-telegram-channel-and-pairing.html",
     "concept": "텔레그램 채널과 페어링",
     "one_line": "입구를 여는 열쇠(토큰)와 누구를 들일지 정하는 열쇠(승인)는 별개다",
     "practice": "폰에서 봇에게 말을 걸게 할 때, 승인 대기 계정을 ID로 직접 확인한 뒤 승인한다",
     "analogy": "아파트 현관과 인터폰",
     "keywords": [
      "BotFather",
      "봇 토큰",
      "pairing",
      "allowlist"
     ],
     "links": [
      "openclaw-session-records-and-usage.html",
      "openclaw-security-boundaries.html"
     ]
    },
    {
     "file": "openclaw-security-boundaries.html",
     "concept": "권한 모드·입구·인젝션",
     "one_line": "파일·명령 범위, 채널 입구, 외부 내용 실행 승인을 각각 다른 문으로 나눈다",
     "practice": "웹 문서를 요약만 시킬 때는 read-only로 시작하고, 파일을 고칠 때만 권한을 올린다",
     "analogy": "호텔 직원의 등급별 마스터키",
     "keywords": [
      "read-only",
      "guarded",
      "프롬프트 인젝션",
      "GHSA"
     ],
     "links": [
      "openclaw-telegram-channel-and-pairing.html",
      "openclaw-multi-agent-bindings.html"
     ]
    },
    {
     "file": "openclaw-multi-agent-bindings.html",
     "concept": "바인딩·델리게이트",
     "one_line": "게이트웨이 하나가 채널 계정을 담당 에이전트에게 나눠 보낸다",
     "practice": "문의 채널마다 담당 에이전트를 나눌 때, 남는 대화를 받을 기본 에이전트를 반드시 지정한다",
     "analogy": "회사 대표번호와 내선 교환원",
     "keywords": [
      "binding",
      "delegate",
      "standing orders",
      "workspace"
     ],
     "links": [
      "openclaw-security-boundaries.html",
      "openclaw-automations-scheduling.html"
     ]
    },
    {
     "file": "openclaw-automations-scheduling.html",
     "concept": "자동화 예약과 cron",
     "one_line": "예약은 SQLite에 남지만 종은 게이트웨이가 켜져 있을 때만 울린다",
     "practice": "매일 아침 손으로 하던 확인을 cron이나 /loop로 예약해 사람이 기억하지 않게 한다",
     "analogy": "학교 종과 시간표",
     "keywords": [
      "cron",
      "automations",
      "/loop",
      "ISO 시각"
     ],
     "links": [
      "openclaw-multi-agent-bindings.html",
      "openclaw-pi-core-and-extensions.html"
     ]
    },
    {
     "file": "openclaw-pi-core-and-extensions.html",
     "concept": "pi 코어와 확장 기능",
     "one_line": "기능을 하나 얹을 때마다 새 입구·기록·권한이 함께 늘어난다",
     "practice": "브라우저 조작이나 메일 감시를 켜기 전에 새 입구·기록·권한 세 줄을 먼저 적는다",
     "analogy": "뼈대만 있는 집과 증축",
     "keywords": [
      "pi",
      "ClawHub",
      "IMAP 감시",
      "실험 단계"
     ],
     "links": [
      "openclaw-automations-scheduling.html"
     ]
    }
   ],
   "name": "OpenClaw — 에이전트 게이트웨이"
  },
  "harness-observe": {
   "sub": "harness-observe",
   "role": "남이 만든 에이전트 하네스를 같은 잣대로 관찰·비교해 도구를 고른다",
   "scenario": "새 코딩 에이전트 도구를 도입하기 전, 일곱 병목 질문과 여섯 칸 관찰 카드로 화면을 직접 뜯어보고 내 병목에 근거 있는 도구만 후보로 남겼다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "일곱 병목 지도",
      "posts": [
       "harness-observation-and-feature-map.html"
      ]
     },
     {
      "id": "n2",
      "label": "포맷·문맥 관찰",
      "posts": [
       "harness-action-format-and-context.html"
      ]
     },
     {
      "id": "n3",
      "label": "경험·반성 관찰",
      "posts": [
       "harness-experience-and-reflection.html"
      ]
     },
     {
      "id": "n4",
      "label": "미니멀·권한 관찰",
      "posts": [
       "harness-minimal-and-permission.html"
      ]
     },
     {
      "id": "n5",
      "label": "도구 비교",
      "posts": [
       "harness-evaluation-and-comparison.html"
      ]
     },
     {
      "id": "n6",
      "label": "불편을 가설로",
      "posts": [
       "harness-hypothesis-experiment.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "관찰하면"
     ],
     [
      "n2",
      "n3",
      "다음 병목"
     ],
     [
      "n3",
      "n4",
      "다음 병목"
     ],
     [
      "n4",
      "n5",
      "일곱 카드 겹치면"
     ],
     [
      "n5",
      "n6",
      "후보 줄이면"
     ]
    ]
   },
   "posts": [
    {
     "file": "harness-observation-and-feature-map.html",
     "concept": "일곱 병목·관찰 카드",
     "one_line": "도구 이름보다 내 일이 어디서 막히는지 일곱 자리로 먼저 짚는다",
     "practice": "새 코딩 에이전트를 쓰기 전에, 같은 fixture로 입력·도구 호출·승인 같은 다섯 신호를 화면에서 찾는다",
     "analogy": "",
     "keywords": [
      "하네스",
      "관찰 카드",
      "fixture",
      "병목"
     ],
     "links": [
      "harness-action-format-and-context.html"
     ]
    },
    {
     "file": "harness-action-format-and-context.html",
     "concept": "행동 포맷·컨텍스트 관리",
     "one_line": "행동을 적는 형식과 문맥에 남길 정보를 고르는 방식이 결과를 가른다",
     "practice": "AI가 엉뚱한 곳을 고치면, 찾을 내용과 바꿀 내용을 짝지은 편집 블록으로 다시 요청한다",
     "analogy": "",
     "keywords": [
      "SWE-agent",
      "ACI",
      "repo map",
      "서브에이전트"
     ],
     "links": [
      "harness-observation-and-feature-map.html",
      "harness-experience-and-reflection.html"
     ]
    },
    {
     "file": "harness-experience-and-reflection.html",
     "concept": "경험 축적과 반성",
     "one_line": "지난 작업을 근거와 다음에 바꿀 구체적 행동으로 압축해야 자산이 된다",
     "practice": "기억해 두라고 시킬 때, 근거와 날짜 없는 단정 문장은 지우거나 조건을 붙인다",
     "analogy": "오답노트",
     "keywords": [
      "ExpeL",
      "Voyager",
      "Reflexion",
      "insight"
     ],
     "links": [
      "harness-action-format-and-context.html",
      "harness-minimal-and-permission.html"
     ]
    },
    {
     "file": "harness-minimal-and-permission.html",
     "concept": "미니멀과 권한·보안",
     "one_line": "가장 작은 루프만 남기고 읽기·실행·외부 입력을 각각 다른 문으로 나눈다",
     "practice": "자료 요약 과업에는 read-only로 시작하고, 파일을 고칠 때만 guarded로 권한을 올린다",
     "analogy": "스위스 나이프 vs 드라이버 하나",
     "keywords": [
      "mini-swe-agent",
      "pi",
      "ToolEmu",
      "격리"
     ],
     "links": [
      "harness-experience-and-reflection.html",
      "harness-evaluation-and-comparison.html"
     ]
    },
    {
     "file": "harness-evaluation-and-comparison.html",
     "concept": "평가 루프·하네스 비교",
     "one_line": "최종 결과와 그에 이른 과정을 함께 봐야 우연한 성공을 가려낸다",
     "practice": "AI 도구를 고를 때, 소개 점수 대신 내 병목 칸에 1차 근거가 있는 도구만 후보로 남긴다",
     "analogy": "",
     "keywords": [
      "trajectory",
      "SWE-bench",
      "관찰 카드",
      "벤더 자체 보고"
     ],
     "links": [
      "harness-minimal-and-permission.html",
      "harness-hypothesis-experiment.html"
     ]
    },
    {
     "file": "harness-hypothesis-experiment.html",
     "concept": "개선 가설과 실험",
     "one_line": "도구에 대한 불편을 한 항목만 바꿔 확인 가능한 가설로 바꾼다",
     "practice": "승인 대기 때문에 멈췄다고 느끼면, 권한 규칙만 조정한 조건과 대조 조건을 같은 과업으로 비교한다",
     "analogy": "",
     "keywords": [
      "반증 가능성",
      "사전 판정식",
      "notes/",
      "Given-When-Then"
     ],
     "links": [
      "harness-evaluation-and-comparison.html"
     ]
    }
   ],
   "name": "에이전트 하네스 — 남의 것을 보는 법"
  },
  "harness-build": {
   "sub": "harness-build",
   "role": "모델-도구 반복 루프를 직접 설계·구현하고 벤치마크로 검증한다",
   "scenario": "PRD부터 시작해 Python으로 파일 읽기·수정 에이전트를 직접 만들고, Terminal-Bench Pro 10문항으로 baseline을 재고 한 항목만 바꿔 개선 실험까지 제출했다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "PRD·사용자 정의",
      "posts": [
       "my-harness-users-and-prd.html"
      ]
     },
     {
      "id": "n2",
      "label": "플랫폼·모델 선택",
      "posts": [
       "my-harness-platform-and-provider.html"
      ]
     },
     {
      "id": "n3",
      "label": "흐름·계약 설계",
      "posts": [
       "my-harness-flow-and-state.html",
       "my-harness-interfaces.html"
      ]
     },
     {
      "id": "n4",
      "label": "완료 조건 정의",
      "posts": [
       "my-harness-acceptance.html"
      ]
     },
     {
      "id": "n5",
      "label": "수직 구현",
      "posts": [
       "my-harness-vertical-slice.html",
       "my-harness-python-code-reading.html"
      ]
     },
     {
      "id": "n6",
      "label": "벤치마크 평가",
      "posts": [
       "my-harness-benchmark-local-port.html",
       "my-harness-scoring-and-report.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "정하면"
     ],
     [
      "n2",
      "n3",
      "고르면"
     ],
     [
      "n3",
      "n4",
      "설계하면"
     ],
     [
      "n4",
      "n5",
      "기준 세우면"
     ],
     [
      "n5",
      "n6",
      "구현하면"
     ]
    ]
   },
   "posts": [
    {
     "file": "my-harness-users-and-prd.html",
     "concept": "하네스 PRD와 사용자",
     "one_line": "모델은 도구를 써 달라 말할 뿐, 실행하고 결과를 돌려주는 건 내 하네스다",
     "practice": "에이전트 만들어 달라고 바로 시키지 않고, 누가·언제·무엇을·무엇을 하면 안 되는지부터 적는다",
     "analogy": "셰프는 창고 열쇠가 없다",
     "keywords": [
      "PRD",
      "OPEN/CHOSEN",
      "도구 호출",
      "실패 삼키기"
     ],
     "links": [
      "my-harness-platform-and-provider.html"
     ]
    },
    {
     "file": "my-harness-platform-and-provider.html",
     "concept": "플랫폼·언어·제공자",
     "one_line": "화면, 하네스 실행 컴퓨터, 모델 실행 컴퓨터는 독립된 세 결정이다",
     "practice": "제공자를 고를 때 이름만 정하지 않고, 연결·호출 형식·결과 전달·내용 품질 네 단계로 나눠 확인한다",
     "analogy": "카페의 주문 자리·주방·로스팅 공장",
     "keywords": [
      "CLI",
      "로컬 웹",
      "OpenAI API",
      "Ollama"
     ],
     "links": [
      "my-harness-users-and-prd.html",
      "my-harness-flow-and-state.html"
     ]
    },
    {
     "file": "my-harness-flow-and-state.html",
     "concept": "실행 흐름·상태·종료 조건",
     "one_line": "상태는 지금 단계를 사용자와 프로그램이 같은 이름으로 구별하는 표시다",
     "practice": "반복 상한에 걸려 멈추면 완료로 표시하지 않고 제한 도달로 중단이라는 별도 상태를 보여준다",
     "analogy": "은행 창구의 전광판",
     "keywords": [
      "승인 대기",
      "계속할 수 있는 오류",
      "반복 상한",
      "세션"
     ],
     "links": [
      "my-harness-platform-and-provider.html",
      "my-harness-interfaces.html"
     ]
    },
    {
     "file": "my-harness-interfaces.html",
     "concept": "API와 도구 인터페이스",
     "one_line": "인터페이스는 무엇을 입력하면 무엇이 돌아오는지에 대한 약속이다",
     "practice": "파일 읽기 도구에서 빈 파일과 못 찾은 파일을 구별되는 오류 코드로 미리 계약해 둔다",
     "analogy": "극장 예매번호",
     "keywords": [
      "작업 ID",
      "어댑터",
      "멱등성",
      "도구 계약"
     ],
     "links": [
      "my-harness-flow-and-state.html",
      "my-harness-acceptance.html"
     ]
    },
    {
     "file": "my-harness-acceptance.html",
     "concept": "완료 조건과 검증 시나리오",
     "one_line": "완료 조건은 구현 전에 무엇을 관찰하면 통과인지 미리 못 박은 기준이다",
     "practice": "코드 수정을 검증할 때 기대값을 함수의 현재 출력이 아니라 규칙에서 직접 계산해 검사에 적는다",
     "analogy": "입주 전 사전점검",
     "keywords": [
      "인수 기준",
      "모의 모델",
      "NOT_RUN/PASS/FAIL",
      "Given-When-Then"
     ],
     "links": [
      "my-harness-interfaces.html",
      "my-harness-vertical-slice.html"
     ]
    },
    {
     "file": "my-harness-vertical-slice.html",
     "concept": "수직 구현과 디버깅",
     "one_line": "도구를 다 만들고 잇지 않고, 작은 요청 하나를 먼저 끝까지 관통시킨다",
     "practice": "에이전트가 안 될 때, 요청 수신부터 최종 답까지 다섯 단계 중 마지막 성공 지점 다음만 고친다",
     "analogy": "물 한 컵을 먼저 흘려 보기",
     "keywords": [
      "수직 구현",
      "모의 응답",
      "환경 변수",
      "막힌 지점"
     ],
     "links": [
      "my-harness-acceptance.html",
      "my-harness-python-code-reading.html"
     ]
    },
    {
     "file": "my-harness-python-code-reading.html",
     "concept": "Python 하네스 읽기",
     "one_line": "모델 연결·도구 실행·판단 반복을 나누면 제공자가 바뀌어도 권한 코드는 그대로다",
     "practice": "루프를 직접 짤지 SDK에 맡길지 고를 때, 루프를 누가 짜는지 네 갈래로 나눠 확인한다",
     "analogy": "신문사 편집국의 자리 배치",
     "keywords": [
      "agent.py",
      "providers.py",
      "tools.py",
      "루프"
     ],
     "links": [
      "my-harness-vertical-slice.html",
      "my-harness-benchmark-local-port.html"
     ]
    },
    {
     "file": "my-harness-benchmark-local-port.html",
     "concept": "벤치마크 10문항 평가",
     "one_line": "벤치마크는 정해진 문제와 남이 정한 채점 기준으로 시스템을 비교하는 방법이다",
     "practice": "쓸 만한지 볼 때, 자체 예제 대신 공개 10문항과 원본 채점 코드를 붙여 baseline을 잰다",
     "analogy": "학교 운동장에서 잰 기록",
     "keywords": [
      "Terminal-Bench Pro",
      "baseline",
      "local-port",
      "verifier"
     ],
     "links": [
      "my-harness-python-code-reading.html",
      "my-harness-scoring-and-report.html"
     ]
    },
    {
     "file": "my-harness-scoring-and-report.html",
     "concept": "점수 읽기와 비교 실험",
     "one_line": "분모는 실제로 시도한 문항 수이며 오류나 미완료가 있어도 줄이지 않는다",
     "practice": "점수가 올랐다고 말하기 전, 모델·한도·커밋을 고정하고 딱 한 항목만 바꿔 baseline과 다시 비교한다",
     "analogy": "영수증 잃어버린 가계부",
     "keywords": [
      "pass/fail/error/pending",
      "회귀 검사",
      "run-metadata",
      "일반화 한계"
     ],
     "links": [
      "my-harness-benchmark-local-port.html"
     ]
    }
   ],
   "name": "에이전트 하네스 — 내 손으로 만들기"
  },
  "web-frontend": {
   "sub": "web-frontend",
   "role": "AI가 만든 화면 코드를 계층별로 검토하고 프레임워크로 정리하는 역할",
   "scenario": "자막 카드가 모바일에서 겹칠 때 클래스명 대신 증상과 조건으로 AI에게 요청하고, 서버 없이 목업 데이터로 먼저 화면을 완성해 본다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "계층 구분",
      "posts": [
       "webpage-three-layers.html"
      ]
     },
     {
      "id": "n2",
      "label": "비동기 이해",
      "posts": [
       "javascript-event-loop-async.html"
      ]
     },
     {
      "id": "n3",
      "label": "게임 실습",
      "posts": [
       "ai-game-making-tetris-to-mine.html"
      ]
     },
     {
      "id": "n4",
      "label": "주소 갈림길",
      "posts": [
       "what-is-routing.html"
      ]
     },
     {
      "id": "n5",
      "label": "API 개념",
      "posts": [
       "what-is-api.html"
      ]
     },
     {
      "id": "n6",
      "label": "프레임워크 선택",
      "posts": [
       "what-is-framework.html",
       "what-is-abstraction-modularity.html",
       "choosing-a-framework.html"
      ]
     },
     {
      "id": "n7",
      "label": "목업으로 화면 완성",
      "posts": [
       "mock-data-and-rest-api.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "동작을 나누면"
     ],
     [
      "n2",
      "n3",
      "실습으로 적용"
     ],
     [
      "n3",
      "n4",
      "배포 뒤 확인"
     ],
     [
      "n4",
      "n5",
      "다른 서버와 통신"
     ],
     [
      "n5",
      "n6",
      "도구 골라 짜기"
     ],
     [
      "n6",
      "n7",
      "목업으로 완성"
     ]
    ]
   },
   "posts": [
    {
     "file": "webpage-three-layers.html",
     "concept": "HTML·CSS·JS 3계층",
     "one_line": "웹페이지는 정보·표현·동작 세 계층이 각각 다른 시대에 태어났다",
     "practice": "AI에게 화면 수정을 요청할 때 어느 계층 문제인지 짚어 말하면 정확히 통한다",
     "analogy": "건물의 골조·인테리어·전기설비",
     "keywords": [
      "HTML",
      "CSS",
      "JavaScript",
      "관심사의 분리"
     ],
     "links": [
      "javascript-event-loop-async.html",
      "ai-game-making-tetris-to-mine.html"
     ]
    },
    {
     "file": "javascript-event-loop-async.html",
     "concept": "동기·비동기와 이벤트 루프",
     "one_line": "자바스크립트는 스레드 하나로 오래 걸리는 일을 걸어두고 넘어가 화면이 안 멈추게 한다",
     "practice": "버튼 클릭 후 서버 응답을 기다릴 때 비동기로 처리해야 화면이 굳지 않는다",
     "analogy": "카페 진동벨",
     "keywords": [
      "동기",
      "비동기",
      "이벤트 루프",
      "시분할"
     ],
     "links": [
      "webpage-three-layers.html",
      "ai-game-making-tetris-to-mine.html"
     ]
    },
    {
     "file": "ai-game-making-tetris-to-mine.html",
     "concept": "규칙을 요청문으로 쪼개기",
     "one_line": "이름난 게임은 이름이 규칙 명세서지만, 내 게임은 규칙을 직접 적어야 한다",
     "practice": "이름 없는 내 아이디어를 AI에게 시킬 때 보이는 것·상태·규칙 표로 채워 요청한다",
     "analogy": "",
     "keywords": [
      "보이는 것",
      "상태",
      "규칙",
      "배포"
     ],
     "links": [
      "javascript-event-loop-async.html",
      "what-is-routing.html"
     ]
    },
    {
     "file": "what-is-routing.html",
     "concept": "라우팅",
     "one_line": "라우팅은 들어온 주소를 보고 어떤 화면을 보여줄지 정하는 갈림길이다",
     "practice": "언어별로 다른 페이지를 보여줄 때 이미 작동 중인 라우팅부터 확인한다",
     "analogy": "우편 분류소",
     "keywords": [
      "라우팅",
      "도메인",
      "브라우저 언어",
      "index.html"
     ],
     "links": [
      "ai-game-making-tetris-to-mine.html",
      "what-is-api.html"
     ]
    },
    {
     "file": "what-is-api.html",
     "concept": "API",
     "one_line": "API는 프로그램끼리 정해진 형식으로 요청하고 답 받는 통로다",
     "practice": "남의 데이터를 내 컴퓨터에 복사하지 않고 필요할 때마다 API로 물어볼 때 쓴다",
     "analogy": "식당 손님·웨이터·주방",
     "keywords": [
      "API",
      "API 문서",
      "서버",
      "오픈API"
     ],
     "links": [
      "what-is-routing.html",
      "what-is-framework.html",
      "mock-data-and-rest-api.html"
     ]
    },
    {
     "file": "what-is-framework.html",
     "concept": "프레임워크",
     "one_line": "프레임워크는 반복·변화·연결을 컴포넌트·상태·라우팅으로 미리 풀어둔 골조다",
     "practice": "화면이 늘고 데이터가 얽힐 때 카드를 복사하는 대신 프레임워크의 컴포넌트로 묶는다",
     "analogy": "집 지을 때의 뼈대",
     "keywords": [
      "프레임워크",
      "컴포넌트",
      "상태",
      "라이브러리"
     ],
     "links": [
      "what-is-api.html",
      "what-is-abstraction-modularity.html"
     ]
    },
    {
     "file": "what-is-abstraction-modularity.html",
     "concept": "추상화와 모듈화",
     "one_line": "추상화는 복잡한 속을 감추고, 모듈화는 갈아 끼울 조각으로 나누는 것이다",
     "practice": "AI에게 '컴포넌트로 만들어 재사용해'처럼 조각과 상태 단위로 지시할 때 통한다",
     "analogy": "자동차 페달·핸들, 레고 블록",
     "keywords": [
      "추상화",
      "모듈화",
      "가상 DOM",
      "선언형 UI"
     ],
     "links": [
      "what-is-framework.html",
      "choosing-a-framework.html"
     ]
    },
    {
     "file": "choosing-a-framework.html",
     "concept": "프레임워크 고르는 법",
     "one_line": "프레임워크 선택은 많이 쓰는 것과 AI가 정확히 짜 주는지를 근거로 비교하는 일이다",
     "practice": "후보에 같은 요청을 세 번 시켜 구조가 비슷하게 나오는지 확인하고 고른다",
     "analogy": "",
     "keywords": [
      "React",
      "Svelte",
      "DesignBench",
      "PRD"
     ],
     "links": [
      "what-is-abstraction-modularity.html",
      "mock-data-and-rest-api.html"
     ]
    },
    {
     "file": "mock-data-and-rest-api.html",
     "concept": "목업 데이터와 REST",
     "one_line": "목업 데이터는 백엔드 없이도 진짜 API와 같은 모양으로 화면부터 완성하게 해준다",
     "practice": "서버가 아직 없을 때 mockData.js를 따로 빼 두면 나중에 fetch 한 줄로 교체된다",
     "analogy": "아파트 모델하우스",
     "keywords": [
      "목업 데이터",
      "REST",
      "GET·POST·PUT·DELETE",
      "GraphQL"
     ],
     "links": [
      "choosing-a-framework.html",
      "why-backend-needed.html"
     ]
    }
   ],
   "name": "웹 구조와 프론트엔드"
  },
  "backend-deploy": {
   "sub": "backend-deploy",
   "role": "화면 뒤에서 요청을 처리하고 안전하게 세상에 내보내는 역할",
   "scenario": "친구에게 링크를 보냈더니 안 열렸던 경험에서 서버를 세우고, API 키를 프록시 서버 뒤에 숨기고 CORS를 열어 무료 플랫폼에 배포한다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "서버 필요성 판단",
      "posts": [
       "why-backend-needed.html"
      ]
     },
     {
      "id": "n2",
      "label": "주소로 서버 찾기",
      "posts": [
       "domain-http-and-packets.html"
      ]
     },
     {
      "id": "n3",
      "label": "요청 처리(CRUD)",
      "posts": [
       "what-backend-actually-does.html"
      ]
     },
     {
      "id": "n4",
      "label": "보안 점검",
      "posts": [
       "ai-code-security-basics.html"
      ]
     },
     {
      "id": "n5",
      "label": "배포",
      "posts": [
       "deploying-and-free-hosting.html",
       "what-is-docker.html"
      ]
     },
     {
      "id": "n6",
      "label": "화면-서버 연결",
      "posts": [
       "connecting-frontend-backend.html"
      ]
     },
     {
      "id": "n7",
      "label": "키 숨기고 문 열기",
      "posts": [
       "what-is-proxy-server.html",
       "what-is-cors.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "요청이 도착"
     ],
     [
      "n2",
      "n3",
      "서버가 처리"
     ],
     [
      "n3",
      "n4",
      "처리 전 점검"
     ],
     [
      "n4",
      "n5",
      "안전해지면 배포"
     ],
     [
      "n5",
      "n6",
      "배포 뒤 연결"
     ],
     [
      "n6",
      "n7",
      "연결 중 키 보호"
     ]
    ]
   },
   "posts": [
    {
     "file": "why-backend-needed.html",
     "concept": "서버(백엔드)",
     "one_line": "서버는 24시간 켜져서 요청을 받아주는, 내 컴퓨터 밖의 컴퓨터다",
     "practice": "새 기능을 기획할 때 '내 컴퓨터를 벗어나야 하나'를 물어 서버 필요 여부를 가늠한다",
     "analogy": "24시간 콜센터 상담원",
     "keywords": [
      "서버",
      "클라이언트",
      "localhost",
      "로드 밸런서"
     ],
     "links": [
      "mock-data-and-rest-api.html",
      "domain-http-and-packets.html"
     ]
    },
    {
     "file": "domain-http-and-packets.html",
     "concept": "도메인·포트·HTTPS",
     "one_line": "도메인은 DNS가 IP로 바꿔주는 이름이고, 주소창 엔터 뒤엔 네 단계가 지나간다",
     "practice": "화면이 안 열릴 때 네트워크 탭의 상태 코드(404·500 등)를 그대로 AI에게 물어본다",
     "analogy": "택배 배송(전화번호부·발송·주문처리·개봉)",
     "keywords": [
      "DNS",
      "포트",
      "HTTPS",
      "상태 코드"
     ],
     "links": [
      "why-backend-needed.html",
      "what-backend-actually-does.html"
     ]
    },
    {
     "file": "what-backend-actually-does.html",
     "concept": "백엔드의 일(CRUD)",
     "one_line": "백엔드는 요청을 받아 처리하고 응답을 돌려주며, 가격은 서버가 다시 계산해야 한다",
     "practice": "결제 기능을 만들 때 최종 금액을 프론트가 보낸 값이 아니라 서버가 재계산하게 한다",
     "analogy": "콜센터 상담원과 매뉴얼",
     "keywords": [
      "엔드포인트",
      "CRUD",
      "REST",
      "비즈니스 로직"
     ],
     "links": [
      "domain-http-and-packets.html",
      "ai-code-security-basics.html"
     ]
    },
    {
     "file": "ai-code-security-basics.html",
     "concept": "AI 코드 보안 점검",
     "one_line": "AI가 짠 코드의 약 45%에 보안 결함이 있어 입력·비밀키·권한을 따로 점검해야 한다",
     "practice": "API 키를 코드에 적지 않고 .env로 빼서 .gitignore로 막을 때 이 원칙을 적용한다",
     "analogy": "콘서트장 표 검사원(인증)과 VIP 바운서(인가)",
     "keywords": [
      "환경변수",
      "인증",
      "인가",
      "해시·솔트"
     ],
     "links": [
      "what-backend-actually-does.html",
      "deploying-and-free-hosting.html"
     ]
    },
    {
     "file": "deploying-and-free-hosting.html",
     "concept": "배포와 무료 호스팅",
     "one_line": "배포는 화면·서버·데이터를 잘하는 무료 플랫폼에 나눠 올려 늘 켜진 서비스로 만드는 일이다",
     "practice": "포트폴리오는 정적 호스팅, 로그인+DB는 Supabase처럼 용도별 무료 서비스를 고를 때 쓴다",
     "analogy": "",
     "keywords": [
      "Vercel",
      "Supabase",
      "RLS",
      "무료 티어"
     ],
     "links": [
      "ai-code-security-basics.html",
      "connecting-frontend-backend.html",
      "what-is-docker.html"
     ]
    },
    {
     "file": "connecting-frontend-backend.html",
     "concept": "프론트-백엔드 연결",
     "one_line": "연결은 목업 데이터를 부르던 코드를 실제 API 호출로 한 겹만 갈아 끼우는 일이다",
     "practice": "화면과 서버를 이을 때 요청·응답 JSON 모양을 명세 문서로 먼저 정해 불일치를 막는다",
     "analogy": "",
     "keywords": [
      "계약 불일치",
      "수직 슬라이스",
      "로딩·에러 상태",
      "환경변수"
     ],
     "links": [
      "deploying-and-free-hosting.html",
      "what-is-proxy-server.html",
      "what-is-cors.html"
     ]
    },
    {
     "file": "what-is-proxy-server.html",
     "concept": "프록시 서버",
     "one_line": "프록시 서버는 브라우저 대신 API 키를 들고 외부 서비스를 불러주는 중계 서버다",
     "practice": "외부 AI를 부를 때 키를 브라우저에 두지 않고 프록시 서버 환경변수에만 두어 감춘다",
     "analogy": "회사 로비의 안내 데스크",
     "keywords": [
      "프록시",
      "API 키",
      "환경변수",
      "중계 서버"
     ],
     "links": [
      "connecting-frontend-backend.html",
      "what-is-cors.html"
     ]
    },
    {
     "file": "what-is-cors.html",
     "concept": "CORS",
     "one_line": "CORS는 다른 주소에서 온 응답을 넘겨도 되는지 브라우저가 검사하는 규칙이다",
     "practice": "화면과 서버 주소가 다를 때 서버 응답에 허용 주소 헤더를 붙여야 브라우저가 통과시킨다",
     "analogy": "국경 검문소의 여권 검사",
     "keywords": [
      "CORS",
      "Access-Control-Allow-Origin",
      "origin",
      "프리플라이트"
     ],
     "links": [
      "what-is-proxy-server.html",
      "connecting-frontend-backend.html"
     ]
    },
    {
     "file": "what-is-docker.html",
     "concept": "도커(이미지·컨테이너)",
     "one_line": "도커는 프로그램과 실행 환경을 상자에 통째로 담아 어느 컴퓨터에서든 같은 조건으로 돌린다",
     "practice": "'내 컴퓨터에선 되는데요' 문제가 생길 때 환경을 상자로 통째로 옮겨 없앤다",
     "analogy": "밀키트 상자",
     "keywords": [
      "이미지",
      "컨테이너",
      "볼륨",
      "Dockerfile"
     ],
     "links": [
      "deploying-and-free-hosting.html",
      "choosing-a-free-database.html"
     ]
    }
   ],
   "name": "백엔드와 배포"
  },
  "database": {
   "sub": "database",
   "role": "데이터를 안전히 저장하고 빠르게 찾아 서비스가 기억을 유지하는 역할",
   "scenario": "새로고침해도 사라지지 않게 회원 표를 설계하고, SQL 주입을 막고 3-2-1 규칙으로 백업을 갖춰 무료 DB를 고른다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "영구 저장 필요성",
      "posts": [
       "why-database-needed.html"
      ]
     },
     {
      "id": "n2",
      "label": "SQL·NoSQL 갈래",
      "posts": [
       "database-history-sql-nosql.html"
      ]
     },
     {
      "id": "n3",
      "label": "표 설계·SQL",
      "posts": [
       "sql-basics-and-table-design.html"
      ]
     },
     {
      "id": "n4",
      "label": "트랜잭션·정규화",
      "posts": [
       "transactions-normalization-nosql-types.html"
      ]
     },
     {
      "id": "n5",
      "label": "회원가입·로그인",
      "posts": [
       "user-accounts-sessions-and-cache.html"
      ]
     },
     {
      "id": "n6",
      "label": "보안·백업",
      "posts": [
       "sql-injection-and-backup-basics.html"
      ]
     },
     {
      "id": "n7",
      "label": "무료 DB 고르기",
      "posts": [
       "choosing-a-free-database.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "종류를 가르면"
     ],
     [
      "n2",
      "n3",
      "표로 설계"
     ],
     [
      "n3",
      "n4",
      "안전 장치 추가"
     ],
     [
      "n4",
      "n5",
      "회원 데이터에 적용"
     ],
     [
      "n5",
      "n6",
      "공격·유실 대비"
     ],
     [
      "n6",
      "n7",
      "지킬 조건으로 고르기"
     ]
    ]
   },
   "posts": [
    {
     "file": "why-database-needed.html",
     "concept": "데이터베이스",
     "one_line": "데이터베이스는 많은 데이터를 저장하고 원하는 것만 빠르게 찾아 주는 곳이다",
     "practice": "새로고침해도 남아야 하는 값을 만들 때 메모리 변수 대신 데이터베이스에 저장한다",
     "analogy": "도서관과 마법 장난감 상자",
     "keywords": [
      "스키마",
      "검색 속도",
      "동시 사용",
      "엑셀과의 차이"
     ],
     "links": [
      "what-is-docker.html",
      "database-history-sql-nosql.html"
     ]
    },
    {
     "file": "database-history-sql-nosql.html",
     "concept": "SQL과 NoSQL",
     "one_line": "데이터베이스 종류가 많은 건 시대마다 병목이 달라 SQL과 NoSQL로 갈렸기 때문이다",
     "practice": "첫 서비스를 시작할 때 관계가 분명한 데이터면 SQL을 기본값으로 고른다",
     "analogy": "",
     "keywords": [
      "관계형",
      "정형·비정형 데이터",
      "폴리글랏",
      "코드"
     ],
     "links": [
      "why-database-needed.html",
      "sql-basics-and-table-design.html"
     ]
    },
    {
     "file": "sql-basics-and-table-design.html",
     "concept": "SQL과 표 설계",
     "one_line": "SQL은 표에서 데이터를 꺼내고 넣으라는 명령이고, 표는 관계로 이어 중복을 없앤다",
     "practice": "표 관계도를 볼 때 '한쪽만 여럿인지 양쪽 다 여럿인지'를 물어 연결 표 필요 여부를 판단한다",
     "analogy": "책 뒤 찾아보기(색인)",
     "keywords": [
      "SELECT",
      "1:N",
      "N:M",
      "색인"
     ],
     "links": [
      "database-history-sql-nosql.html",
      "transactions-normalization-nosql-types.html"
     ]
    },
    {
     "file": "transactions-normalization-nosql-types.html",
     "concept": "트랜잭션과 정규화",
     "one_line": "트랜잭션은 여러 동작을 묶어 전부 되거나 전부 안 되게 만드는 안전장치다",
     "practice": "결제·재고처럼 동시에 눌릴 수 있는 기능을 AI에게 맡길 때 동시 요청 테스트까지 요구한다",
     "analogy": "계좌 이체 중 정전",
     "keywords": [
      "ACID",
      "정규화",
      "마이그레이션",
      "NoSQL 네 갈래"
     ],
     "links": [
      "sql-basics-and-table-design.html",
      "user-accounts-sessions-and-cache.html"
     ]
    },
    {
     "file": "user-accounts-sessions-and-cache.html",
     "concept": "회원가입·로그인 데이터",
     "one_line": "로그인은 회원 표의 행과 입력값을 대조하는 일이고, 유지는 세션이나 토큰이 한다",
     "practice": "로그인 기능을 만들 때 비밀번호 칸이 해시로 저장되는지, 토큰에 민감정보가 없는지 확인한다",
     "analogy": "",
     "keywords": [
      "password_hash",
      "세션",
      "JWT",
      "Redis 캐시"
     ],
     "links": [
      "transactions-normalization-nosql-types.html",
      "sql-injection-and-backup-basics.html"
     ]
    },
    {
     "file": "sql-injection-and-backup-basics.html",
     "concept": "SQL 주입과 백업",
     "one_line": "SQL 주입은 입력값이 명령으로 실행돼 데이터를 지우거나 빼내는 공격이다",
     "practice": "DB에 값을 넣을 때 문자열을 이어 붙이지 않고 파라미터화 쿼리로 처리해 주입을 막는다",
     "analogy": "Little Bobby Tables 만화",
     "keywords": [
      "SQL 주입",
      "파라미터화 쿼리",
      "3-2-1 백업",
      "개인정보 최소 수집"
     ],
     "links": [
      "user-accounts-sessions-and-cache.html",
      "choosing-a-free-database.html"
     ]
    },
    {
     "file": "choosing-a-free-database.html",
     "concept": "무료 데이터베이스 고르기",
     "one_line": "무료 DB 고르기는 필요한 기능, 용량 한도, 미사용 시 정지 여부를 따지는 일이다",
     "practice": "발표 직전 앱이 멈추지 않도록 가입 직전 공식 가격 페이지에서 무료 한도를 다시 확인한다",
     "analogy": "",
     "keywords": [
      "Supabase",
      "Neon",
      "Turso",
      "SQLite"
     ],
     "links": [
      "sql-injection-and-backup-basics.html",
      "what-is-docker.html"
     ]
    }
   ],
   "name": "데이터베이스"
  },
  "work-with-ai": {
   "sub": "work-with-ai",
   "role": "AI 프로젝트 착수 전 사람이 내리는 판단들",
   "scenario": "AIFFEL 과정에서 도메인 지식으로 AI 답을 O/△/X로 채점하고, PoC로 업무 병목을 확인하고, 네 동작으로 업무를 쪼개 AI에게 넘기고, 메인 퀘스트에서 하나는 끝까지 되는 MVP를 완성해 나간다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "도메인 감각 확인",
      "posts": [
       "domain-expertise-ai-era-asset.html"
      ]
     },
     {
      "id": "n2",
      "label": "PoC로 병목 진단",
      "posts": [
       "ai-poc-and-application-judgment.html"
      ]
     },
     {
      "id": "n3",
      "label": "네 동작 분해",
      "posts": [
       "computational-thinking-for-prompting.html"
      ]
     },
     {
      "id": "n4",
      "label": "AI에게 위임",
      "posts": [
       "computational-thinking-for-prompting.html"
      ]
     },
     {
      "id": "n5",
      "label": "MVP로 좁히기",
      "posts": [
       "mainquest-mvp-and-doom-loop.html"
      ]
     },
     {
      "id": "n6",
      "label": "막히면 되돌리기",
      "posts": [
       "mainquest-mvp-and-doom-loop.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "병목 찾기"
     ],
     [
      "n2",
      "n3",
      "조각내기"
     ],
     [
      "n3",
      "n4",
      "맡기기"
     ],
     [
      "n4",
      "n5",
      "쌓기"
     ],
     [
      "n5",
      "n6",
      "막히면"
     ]
    ]
   },
   "posts": [
    {
     "file": "domain-expertise-ai-era-asset.html",
     "concept": "도메인 전문성",
     "one_line": "AI가 못 푸는 문제·판단·신뢰는 도메인 전문가만의 무기다",
     "practice": "AI 답변을 그대로 믿지 않고 O/△/X로 채점할 때, 도메인 지식으로 틀린 곳을 짚어낸다",
     "analogy": "",
     "keywords": [
      "도메인 전문성",
      "환각",
      "비대칭 우위",
      "결합 패턴"
     ],
     "links": [
      "choosing-a-free-database.html",
      "ai-poc-and-application-judgment.html"
     ]
    },
    {
     "file": "ai-poc-and-application-judgment.html",
     "concept": "PoC 판단 기준",
     "one_line": "PoC는 완성품이 아니라 구축할 가치를 판단하려 최소로 만드는 단계다",
     "practice": "정확도로 도입 근거를 잡으려 할 때, 사람이 이미 더 정확한지부터 확인한다",
     "analogy": "",
     "keywords": [
      "PoC",
      "네 업무 유형",
      "성공 기준",
      "병목"
     ],
     "links": [
      "domain-expertise-ai-era-asset.html",
      "computational-thinking-for-prompting.html",
      "object-detection-and-iou.html",
      "why-cant-ai-read-this-pdf.html"
     ]
    },
    {
     "file": "computational-thinking-for-prompting.html",
     "concept": "컴퓨팅 사고법",
     "one_line": "큰 문제를 분해·패턴 인식·추상화·알고리즘 네 동작으로 쪼개 AI에게 넘긴다",
     "practice": "AI에게 '업무 자동화해줘'처럼 뭉뚱그려 부탁해 엉뚱한 답이 올 때, 네 동작으로 쪼개 다시 시킨다",
     "analogy": "결혼식 준비를 통째로 던지듯 막연히 부탁하기",
     "keywords": [
      "분해",
      "패턴 인식",
      "추상화",
      "알고리즘"
     ],
     "links": [
      "ai-poc-and-application-judgment.html",
      "mainquest-mvp-and-doom-loop.html",
      "domain-expertise-ai-era-asset.html"
     ]
    },
    {
     "file": "mainquest-mvp-and-doom-loop.html",
     "concept": "MVP와 둠 루프",
     "one_line": "MVP는 완벽한 작은 버전이 아니라 하나는 끝까지 되는 버전이다",
     "practice": "AI가 '고쳤다'는데 같은 버그가 반복될 때, 막히면 마지막 커밋으로 되돌리고 새 대화로 시작한다",
     "analogy": "고무 오리에게 설명하는 러버덕 디버깅",
     "keywords": [
      "MVP",
      "둠 루프",
      "커밋",
      "러버덕 디버깅"
     ],
     "links": [
      "computational-thinking-for-prompting.html",
      "what-is-prompt-engineering.html",
      "ai-code-security-basics.html",
      "rag-chatbot-prd-questions.html"
     ]
    }
   ],
   "name": "AI와 함께 일하는 법"
  },
  "prompt-agent-concepts": {
   "sub": "prompt-agent-concepts",
   "role": "AI 실행 조건을 설계해 결과를 예측·검증하는 법",
   "scenario": "항공사 챗봇이 규정을 잘못 안내해 배상 판결을 받은 사례처럼, 지시·맥락·도구·루프 중 무엇이 빠졌는지 확인하고, 컨텍스트를 설계하고, 유명한 기법을 내 환경에서 재검증해 에이전트를 안전하게 굴린다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "네 조건 설계",
      "posts": [
       "what-is-prompt-engineering.html"
      ]
     },
     {
      "id": "n2",
      "label": "하네스로 연결",
      "posts": [
       "what-is-ai-agent.html"
      ]
     },
     {
      "id": "n3",
      "label": "입력 출처 구분",
      "posts": [
       "what-is-model-input.html"
      ]
     },
     {
      "id": "n4",
      "label": "컨텍스트 설계",
      "posts": [
       "context-engineering-basics.html"
      ]
     },
     {
      "id": "n5",
      "label": "기법 재검증",
      "posts": [
       "prompt-engineering-history.html",
       "prompt-technique-verification.html"
      ]
     },
     {
      "id": "n6",
      "label": "자기개선 루프",
      "posts": [
       "agent-self-improvement-complexity.html"
      ]
     },
     {
      "id": "n7",
      "label": "실전 실행",
      "posts": [
       "ai-agent-beginner-guide.html",
       "prompt-execution-three-paths.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "하네스로"
     ],
     [
      "n2",
      "n3",
      "입력 분해"
     ],
     [
      "n3",
      "n4",
      "맥락 담기"
     ],
     [
      "n4",
      "n5",
      "재검증"
     ],
     [
      "n5",
      "n6",
      "교훈 남김"
     ],
     [
      "n6",
      "n7",
      "실행 확인"
     ]
    ]
   },
   "posts": [
    {
     "file": "what-is-prompt-engineering.html",
     "concept": "지시·맥락·도구·루프",
     "one_line": "AI 답의 질은 문구가 아니라 지시·맥락·도구·루프 네 조건이 함께 정한다",
     "practice": "AI 답이 계속 나쁠 때, 네 조건 중 하나만 바꿔가며 원인을 좁힌다",
     "analogy": "규정집 없이 알바생에게 '알아서 잘해'라고 시키는 것",
     "keywords": [
      "프롬프트 엔지니어링",
      "지시",
      "맥락",
      "루프"
     ],
     "links": [
      "what-is-ai-agent.html",
      "terminal-shell-kernel-prompt.html",
      "ai-agent-beginner-guide.html",
      "vibe-coding-loop.html"
     ]
    },
    {
     "file": "what-is-ai-agent.html",
     "concept": "에이전트=모델+하네스",
     "one_line": "에이전트는 상황을 관찰하고 스스로 다음 행동을 판단해 반복하는 시스템이다",
     "practice": "AI가 '수정했습니다'라고 보고할 때, 그 말을 믿지 말고 테스트를 직접 돌려 확인한다",
     "analogy": "말에 채우는 마구(하네스)가 힘을 마차로 옮기는 것",
     "keywords": [
      "에이전트",
      "워크플로",
      "하네스",
      "관측"
     ],
     "links": [
      "what-is-prompt-engineering.html",
      "what-is-model-input.html",
      "what-is-vibe-coding.html"
     ]
    },
    {
     "file": "what-is-model-input.html",
     "concept": "모델 입력 4역할",
     "one_line": "모델이 읽는 입력은 시스템·개발자·사용자·외부데이터가 섞인 묶음 전체다",
     "practice": "AI가 읽어온 문서에 '규칙을 무시하라'는 문장이 있을 때, 지시가 아니라 그냥 읽을 자료로 취급한다",
     "analogy": "안내데스크 직원이 방침·지침·접수 일지를 함께 보는 것",
     "keywords": [
      "프롬프트 인젝션",
      "출처",
      "기능",
      "대화 이력"
     ],
     "links": [
      "what-is-ai-agent.html",
      "context-engineering-basics.html"
     ]
    },
    {
     "file": "context-engineering-basics.html",
     "concept": "컨텍스트 엔지니어링",
     "one_line": "무엇을 얼마나 보여줄지 골라 담는 일이 컨텍스트 엔지니어링이다",
     "practice": "사내 규정 챗봇이 없는 답을 지어낼 때, 통째 투입·RAG·just-in-time 중 전달 방식을 점검한다",
     "analogy": "뉴스 앵커에게 방송 규정·지침·요청이 동시에 뜨는 것",
     "keywords": [
      "Instruction Hierarchy",
      "RAG",
      "우선권",
      "컨텍스트 창"
     ],
     "links": [
      "what-is-model-input.html",
      "prompt-engineering-history.html"
     ]
    },
    {
     "file": "prompt-engineering-history.html",
     "concept": "프롬프트 기법 역사",
     "one_line": "프롬프트 기법은 예시 계약→추론 형식→시스템 설계→조건 설계로 대상이 넓어졌다",
     "practice": "'단계별로 생각해봐'를 최신 추론 모델에 붙이려 할 때, 오히려 방해될 수 있으니 먼저 비교해 본다",
     "analogy": "",
     "keywords": [
      "CoT",
      "few-shot",
      "ReAct",
      "thinking budget"
     ],
     "links": [
      "context-engineering-basics.html",
      "prompt-technique-verification.html"
     ]
    },
    {
     "file": "prompt-technique-verification.html",
     "concept": "기법 재검증 3등급",
     "one_line": "유명한 기법도 확고·조건부·논쟁 중으로 등급을 매겨 내 환경에서 재확인해야 한다",
     "practice": "새 프롬프트 기법을 도입할 때, 기준선을 먼저 돌리고 조건 하나만 바꿔 비교한다",
     "analogy": "'8kg 감량!' 다이어트 기사에 붙은 숨은 조건들",
     "keywords": [
      "증거 등급",
      "홀드아웃",
      "컨텍스트 엔지니어링",
      "agentic"
     ],
     "links": [
      "prompt-engineering-history.html",
      "agent-self-improvement-complexity.html"
     ]
    },
    {
     "file": "agent-self-improvement-complexity.html",
     "concept": "자기개선과 복잡도",
     "one_line": "에이전트 자기개선은 모델이 아니라 다음 시도가 읽을 메모가 쌓이는 것이다",
     "practice": "같은 실패가 실제로 반복될 때만, 0→1→2→3단계로 구조를 한 칸씩 올린다",
     "analogy": "시험에서 틀린 걸 적어두는 오답 노트",
     "keywords": [
      "Reflexion",
      "복잡도 사다리",
      "회귀",
      "컴파운드 엔지니어링"
     ],
     "links": [
      "prompt-technique-verification.html",
      "ai-agent-beginner-guide.html"
     ]
    },
    {
     "file": "ai-agent-beginner-guide.html",
     "concept": "신입 비서 2주 비유",
     "one_line": "신입 비서를 2주간 훈련시키는 이야기로 프롬프트~에이전트 시리즈를 다시 훑는다",
     "practice": "동료에게 에이전트가 뭔지 짧게 설명해야 할 때, 이 신입 비서 비유를 그대로 쓴다",
     "analogy": "신입 비서를 채용해 2주간 손발을 맞추는 이야기",
     "keywords": [
      "프롬프트 인젝션",
      "컨텍스트 엔지니어링",
      "권한 사다리",
      "워크플로"
     ],
     "links": [
      "what-is-prompt-engineering.html",
      "agent-self-improvement-complexity.html",
      "prompt-execution-three-paths.html"
     ]
    },
    {
     "file": "prompt-execution-three-paths.html",
     "concept": "세 실행 경로 비교",
     "one_line": "같은 system 지시도 SDK·LangChain·Ollama마다 받는 자료형이 다르다",
     "practice": "system 문구를 바꿔 답이 달라지는지 확인하고 싶을 때, 질문은 고정하고 system만 바꿔 실측한다",
     "analogy": "",
     "keywords": [
      "Claude Agent SDK",
      "LangChain",
      "Ollama",
      "system 지시"
     ],
     "links": [
      "ai-agent-beginner-guide.html",
      "running-local-llm-with-ollama.html",
      "agent-react-loop-and-autogpt.html"
     ]
    }
   ],
   "name": "프롬프트와 에이전트 개념"
  },
  "agent-tools": {
   "sub": "agent-tools",
   "role": "에이전트에 도구·기억·권한을 붙여 힘을 싣는다",
   "scenario": "ReAct 루프로 반복하는 에이전트에 MCP로 내 데이터를 연결하고, 반복 작업은 스킬로 외워두고, 파일 삭제·배포 같은 위험한 행동 앞에서는 승인 모드로 권한을 제한한다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "ReAct 루프",
      "posts": [
       "agent-react-loop-and-autogpt.html"
      ]
     },
     {
      "id": "n2",
      "label": "MCP로 연결",
      "posts": [
       "mcp-usb-c-for-ai.html"
      ]
     },
     {
      "id": "n3",
      "label": "스킬로 외우기",
      "posts": [
       "ai-skills-and-rules-files.html"
      ]
     },
     {
      "id": "n4",
      "label": "권한·비용 관리",
      "posts": [
       "ai-permissions-local-models-and-token-cost.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "도구 연결"
     ],
     [
      "n2",
      "n3",
      "반복 저장"
     ],
     [
      "n3",
      "n4",
      "권한 설정"
     ]
    ]
   },
   "posts": [
    {
     "file": "agent-react-loop-and-autogpt.html",
     "concept": "ReAct 루프",
     "one_line": "에이전트는 계획-실행-관찰-반성을 목표 달성까지 반복한다",
     "practice": "'로그인 오류 고쳐줘'라고 시킬 때, 먼저 로그를 확인하고 수정 뒤 테스트 결과를 보고하게 시킨다",
     "analogy": "품질관리 PDCA, 공군 전략 OODA와 같은 모양",
     "keywords": [
      "ReAct",
      "PDCA",
      "AutoGPT",
      "계획-실행-관찰-반성"
     ],
     "links": [
      "prompt-execution-three-paths.html",
      "mcp-usb-c-for-ai.html"
     ]
    },
    {
     "file": "mcp-usb-c-for-ai.html",
     "concept": "MCP = AI용 USB-C",
     "one_line": "MCP는 AI 앱과 데이터 서비스를 M+N개 연결로 줄여주는 공통 규격이다",
     "practice": "새 MCP 서버를 설정 파일에서 발견했을 때, 공식 문서에 있는 서버인지부터 확인한다",
     "analogy": "기기마다 다르던 충전기가 USB-C 하나로 통일된 것",
     "keywords": [
      "MCP",
      "M×N 문제",
      "Tools",
      "Resources"
     ],
     "links": [
      "agent-react-loop-and-autogpt.html",
      "ai-skills-and-rules-files.html"
     ]
    },
    {
     "file": "ai-skills-and-rules-files.html",
     "concept": "스킬과 규칙 파일",
     "one_line": "스킬은 반복 작업을 적어 두고 꺼내 쓰는 설명서, 규칙 파일은 상시 안내문이다",
     "practice": "브랜드 톤 다듬기처럼 매번 같은 설명을 반복할 때, SKILL.md 한 장으로 적어 재사용한다",
     "analogy": "선반에서 꺼내 쓰는 방법서 vs 상시 안내문",
     "keywords": [
      "SKILL.md",
      "점진 공개",
      "AGENTS.md",
      "CLAUDE.md"
     ],
     "links": [
      "mcp-usb-c-for-ai.html",
      "ai-permissions-local-models-and-token-cost.html"
     ]
    },
    {
     "file": "ai-permissions-local-models-and-token-cost.html",
     "concept": "권한·로컬모델·토큰비용",
     "one_line": "에이전트 권한은 행동 전 사람이 허락할 범위를 정하는 일이다",
     "practice": "문서·회사 자료 폴더에서 에이전트를 켤 때, 자동 수락 대신 매번 확인 모드로 바꾼다",
     "analogy": "",
     "keywords": [
      "승인 모드",
      "로컬 모델",
      "컨텍스트 부패",
      "토큰 비용"
     ],
     "links": [
      "ai-skills-and-rules-files.html",
      "choosing-ai-coding-tools.html"
     ]
    }
   ],
   "name": "에이전트 도구 기초"
  },
  "coding-agent-tools": {
   "sub": "coding-agent-tools",
   "role": "코딩 도구를 고르고 경험을 다음 작업에 쌓는다",
   "scenario": "터미널·편집기·브라우저·클라우드 중 상황에 맞는 코딩 도구를 고르고, 명세 문서로 의도를 먼저 적고, 버그를 고친 교훈을 규칙 파일에 남겨 다음 작업이 이전 작업 위에 쌓이게 한다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "도구 형태 고르기",
      "posts": [
       "choosing-ai-coding-tools.html"
      ]
     },
     {
      "id": "n2",
      "label": "플러그인 세팅",
      "posts": [
       "claude-plugins-and-spec-driven-development.html"
      ]
     },
     {
      "id": "n3",
      "label": "명세 먼저 적기",
      "posts": [
       "claude-plugins-and-spec-driven-development.html"
      ]
     },
     {
      "id": "n4",
      "label": "경험을 규칙에",
      "posts": [
       "compound-engineering-and-loop-engineering.html"
      ]
     },
     {
      "id": "n5",
      "label": "모델 고르기",
      "posts": [
       "opencode-models-and-muse-spark.html"
      ]
     },
     {
      "id": "n6",
      "label": "역할별 팀 구성",
      "posts": [
       "opencode-sisyphus-orchestration.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "세팅 공유"
     ],
     [
      "n2",
      "n3",
      "의도 적기"
     ],
     [
      "n3",
      "n4",
      "루프 반복"
     ],
     [
      "n4",
      "n5",
      "모델 선택"
     ],
     [
      "n5",
      "n6",
      "역할 분담"
     ]
    ]
   },
   "posts": [
    {
     "file": "choosing-ai-coding-tools.html",
     "concept": "코딩 도구 4부류",
     "one_line": "AI 코딩 도구는 터미널·편집기·브라우저·클라우드 네 부류로 나뉜다",
     "practice": "새 코딩 도구를 처음 쓸 때, 되돌리기 쉬운 작은 수정으로 먼저 시험해 본다",
     "analogy": "코파일럿은 회사가, 나머진 엔지니어가 고른다는 우스개",
     "keywords": [
      "터미널형",
      "편집기형",
      "브라우저형",
      "클라우드형"
     ],
     "links": [
      "ai-permissions-local-models-and-token-cost.html",
      "claude-plugins-and-spec-driven-development.html"
     ]
    },
    {
     "file": "claude-plugins-and-spec-driven-development.html",
     "concept": "플러그인과 명세 개발",
     "one_line": "플러그인은 스킬·MCP·명령 묶음, 명세 주도 개발은 의도를 코드보다 먼저 적는 방법이다",
     "practice": "팀의 코드 리뷰 규칙을 공유하고 싶을 때, 플러그인 하나로 묶어 설치 한 줄로 넘긴다",
     "analogy": "",
     "keywords": [
      "플러그인",
      "명세 주도 개발",
      "Spec Kit",
      "PRD"
     ],
     "links": [
      "choosing-ai-coding-tools.html",
      "compound-engineering-and-loop-engineering.html"
     ]
    },
    {
     "file": "compound-engineering-and-loop-engineering.html",
     "concept": "컴파운드 엔지니어링",
     "one_line": "일할 때마다 경험을 규칙·스킬로 남겨 다음 작업이 이전 작업 위에 쌓이게 한다",
     "practice": "AI가 지난주 고친 버그를 또 만들 때, 그 교훈을 AGENTS.md에 적어 자동으로 지키게 한다",
     "analogy": "",
     "keywords": [
      "컴파운드 엔지니어링",
      "Ralph",
      "컨텍스트 부패",
      "CLI vs MCP"
     ],
     "links": [
      "claude-plugins-and-spec-driven-development.html",
      "opencode-models-and-muse-spark.html"
     ]
    },
    {
     "file": "opencode-models-and-muse-spark.html",
     "concept": "모델 선택 4축",
     "one_line": "opencode 모델 목록은 제공자·모델·요금제·추론강도 네 축이 곱해진 것이다",
     "practice": "무료 모델이 보여 반가울 때, 업무 폴더가 아니라 연습 폴더에서만 contributor-free를 쓴다",
     "analogy": "기차표 앱에서 열차는 넷인데 줄이 마흔 줄인 것",
     "keywords": [
      "opencode",
      "Muse Spark",
      "Contributor 티어",
      "모델 캐시"
     ],
     "links": [
      "choosing-ai-coding-tools.html",
      "opencode-sisyphus-orchestration.html"
     ]
    },
    {
     "file": "opencode-sisyphus-orchestration.html",
     "concept": "Sisyphus 역할 분담",
     "one_line": "Sisyphus는 코딩 에이전트를 계획·조율·실행 역할로 쪼개 역할마다 다른 모델을 붙인다",
     "practice": "여러 파일을 건드려야 끝나는 큰 과제를 맡길 때, 첫 실행은 전권 대신 계획 모드로 확인한다",
     "analogy": "신문 편집국의 기획 회의·데스크·편집장 역할 분담",
     "keywords": [
      "Sisyphus",
      "oh-my-openagent",
      "오케스트레이터-워커",
      "역할별 모델"
     ],
     "links": [
      "opencode-models-and-muse-spark.html",
      "what-is-automation-workflow-agent.html"
     ]
    }
   ],
   "name": "코딩 에이전트와 협업 도구"
  },
  "automation-n8n": {
   "sub": "automation-n8n",
   "role": "노코드로 자동화·워크플로·에이전트 경계 굿기",
   "scenario": "메일함에 쌓인 반복 문의 처리를 n8n으로 직접 그려보고, IF 노드와 AI Agent 노드를 나눠 쓰고, 내 컴퓨터에 셀프 호스팅해 운영 책임까지 넘겨받는다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "세 갈래 구분",
      "posts": [
       "what-is-automation-workflow-agent.html"
      ]
     },
     {
      "id": "n2",
      "label": "n8n으로 그리기",
      "posts": [
       "what-is-automation-workflow-agent.html"
      ]
     },
     {
      "id": "n3",
      "label": "에이전트에 위임",
      "posts": [
       "n8n-agent-delegation-and-if-node.html"
      ]
     },
     {
      "id": "n4",
      "label": "IF/Agent 나누기",
      "posts": [
       "n8n-agent-delegation-and-if-node.html"
      ]
     },
     {
      "id": "n5",
      "label": "Webhook 공개",
      "posts": [
       "n8n-agent-delegation-and-if-node.html"
      ]
     },
     {
      "id": "n6",
      "label": "셀프 호스팅 운영",
      "posts": [
       "n8n-self-hosting-options.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "직접 그리기"
     ],
     [
      "n2",
      "n3",
      "CLI로 위임"
     ],
     [
      "n3",
      "n4",
      "갈림길 나눔"
     ],
     [
      "n4",
      "n5",
      "웹에 연결"
     ],
     [
      "n5",
      "n6",
      "직접 운영"
     ]
    ]
   },
   "posts": [
    {
     "file": "what-is-automation-workflow-agent.html",
     "concept": "자동화·워크플로·에이전트",
     "one_line": "다음에 뭘 할지 누가 정하느냐로 자동화·워크플로·에이전트가 갈린다",
     "practice": "업무를 '무조건·항상·매번'으로 설명할 수 있는지 시험해, 안 되면 에이전트로 넘긴다",
     "analogy": "버스 노선 vs 내비게이션 경로 vs 자율주행",
     "keywords": [
      "자동화",
      "워크플로",
      "에이전트",
      "n8n"
     ],
     "links": [
      "opencode-sisyphus-orchestration.html",
      "n8n-agent-delegation-and-if-node.html"
     ]
    },
    {
     "file": "n8n-agent-delegation-and-if-node.html",
     "concept": "IF 노드와 AI Agent",
     "one_line": "값·상태 검사는 IF 노드, 의도 해석은 AI Agent 노드에 나눠 맡긴다",
     "practice": "웹사이트에 AI 응답을 붙일 때, 키는 Credential에 두고 Webhook 주소만 호출하게 한다",
     "analogy": "",
     "keywords": [
      "IF 노드",
      "AI Agent 노드",
      "Webhook",
      "n8n CLI"
     ],
     "links": [
      "what-is-automation-workflow-agent.html",
      "n8n-self-hosting-options.html",
      "ai-code-security-basics.html"
     ]
    },
    {
     "file": "n8n-self-hosting-options.html",
     "concept": "셀프 호스팅 규모 선택",
     "one_line": "셀프 호스팅은 데이터 보관·백업·장애 대응까지 내 책임이 되는 일이다",
     "practice": "n8n을 Docker로 처음 띄울 때, 실행 뒤 사용한 이미지·포트·볼륨을 직접 다시 읽어 확인한다",
     "analogy": "",
     "keywords": [
      "셀프 호스팅",
      "Docker",
      "SQLite vs PostgreSQL",
      "queue mode"
     ],
     "links": [
      "n8n-agent-delegation-and-if-node.html",
      "what-is-docker.html"
     ]
    }
   ],
   "name": "자동화 워크플로 — n8n"
  },
  "ml-basics": {
   "sub": "ml-basics",
   "role": "코딩 에이전트가 짠 학습·분류 코드를 검증하는 기초 판단력",
   "scenario": "코딩 에이전트에게 PyTorch로 MNIST 분류기를 만들게 하고, softmax 확률 합이 1인지·학습 데이터를 10%로 줄이면 정확도가 왜 떨어지는지를 직접 확인해 무엇을 시키고 무엇을 검증할지 판단한 실습이다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "코드 읽기",
      "posts": [
       "reading-python-code-basics.html"
      ]
     },
     {
      "id": "n2",
      "label": "데이터 숫자화",
      "posts": [
       "turning-data-into-numbers.html"
      ]
     },
     {
      "id": "n3",
      "label": "예측-오차-조정 반복",
      "posts": [
       "how-ai-learns-from-data.html",
       "smallest-learning-in-code.html"
      ]
     },
     {
      "id": "n4",
      "label": "분류·확률",
      "posts": [
       "softmax-and-mnist-classification.html"
      ]
     },
     {
      "id": "n5",
      "label": "성능 채점",
      "posts": [
       "confusion-matrix-and-metrics.html"
      ]
     },
     {
      "id": "n6",
      "label": "남의 모델 물려받기",
      "posts": [
       "fine-tuning-and-transfer-learning.html"
      ]
     },
     {
      "id": "n7",
      "label": "하드웨어 판단",
      "posts": [
       "why-gpu-and-colab-cli.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "숫자로 바꿔"
     ],
     [
      "n2",
      "n3",
      "반복 학습해"
     ],
     [
      "n3",
      "n4",
      "분류에 써"
     ],
     [
      "n4",
      "n5",
      "채점해"
     ],
     [
      "n5",
      "n6",
      "물려받아"
     ],
     [
      "n6",
      "n7",
      "장비 따져"
     ]
    ]
   },
   "posts": [
    {
     "file": "reading-python-code-basics.html",
     "concept": "코드 읽기 열 가지 문법",
     "one_line": "코드를 열 가지 문법 단위로 나눠 한 줄씩 한국어로 옮겨 읽는다",
     "practice": "AI가 짜준 코드를 검토할 때 한 줄씩 한국어로 옮겨 뜻을 확인한다",
     "analogy": "국 끓이는 동안 다른 일 하기",
     "keywords": [
      "변수",
      "함수",
      "try/except",
      "async",
      "가상환경"
     ],
     "links": [
      "javascript-event-loop-async.html",
      "terminal-practice.html",
      "multi-agent-three-runs-abc.html",
      "prompt-execution-three-paths.html"
     ]
    },
    {
     "file": "how-ai-learns-from-data.html",
     "concept": "예측-오차-조정 학습 고리",
     "one_line": "AI 학습은 예측하고 틀린 정도를 재고 숫자를 조금씩 고치는 반복이다",
     "practice": "코딩 에이전트에게 판단 로직을 맡길 때 규칙 코드인지 데이터 학습인지를 가른다",
     "analogy": "신입이 계약서 1,000건 보며 감을 익히는 것",
     "keywords": [
      "지도학습",
      "경사하강",
      "가중치",
      "일반화",
      "오차"
     ],
     "links": [
      "reading-python-code-basics.html",
      "turning-data-into-numbers.html"
     ]
    },
    {
     "file": "turning-data-into-numbers.html",
     "concept": "벡터·텐서 표현",
     "one_line": "글과 그림은 토큰·픽셀로 쪼개져 숫자 벡터·텐서가 된다",
     "practice": "손글씨 숫자 한 장이 왜 784개 숫자로 표현되는지 설명할 때 이 사다리를 쓴다",
     "analogy": "서울-인천은 가깝고 서울-부산은 먼 것처럼 잰다",
     "keywords": [
      "토큰",
      "임베딩",
      "벡터",
      "텐서",
      "픽셀"
     ],
     "links": [
      "how-ai-learns-from-data.html",
      "smallest-learning-in-code.html"
     ]
    },
    {
     "file": "smallest-learning-in-code.html",
     "concept": "카페 매출 예측 실습",
     "one_line": "weight·bias 두 숫자만으로 경사하강이 실제로 하는 일을 코드로 본다",
     "practice": "학습 결과가 이상해 보일 때 데이터 중심에서 먼 값(절편)이 더 흔들리는지 확인한다",
     "analogy": "방문객 100명 늘면 매출 207만원 느는 기울기",
     "keywords": [
      "torch",
      "경사하강",
      "autograd",
      "가중치",
      "절편"
     ],
     "links": [
      "turning-data-into-numbers.html",
      "softmax-and-mnist-classification.html"
     ]
    },
    {
     "file": "softmax-and-mnist-classification.html",
     "concept": "softmax 확률 변환",
     "one_line": "softmax는 점수를 exp와 합으로 나눠 합이 1인 확률로 바꾼다",
     "practice": "분류기를 에이전트에 맡길 때 확률 합이 1인지, 손실 함수와 이중 적용은 없는지 확인한다",
     "analogy": "hard max와 달리 작은 값에도 확률을 남기는 것",
     "keywords": [
      "softmax",
      "MNIST",
      "로짓",
      "CrossEntropyLoss",
      "확신도"
     ],
     "links": [
      "smallest-learning-in-code.html",
      "confusion-matrix-and-metrics.html"
     ]
    },
    {
     "file": "confusion-matrix-and-metrics.html",
     "concept": "혼동 행렬·정밀도·재현율",
     "one_line": "네 칸(TP·FP·FN·TN)으로 나눠 세고, 분모만 다르게 봐 세 지표를 구한다",
     "practice": "정확도 숫자만 보고받았을 때 데이터 불균형으로 숫자가 부풀었는지 되묻는다",
     "analogy": "편지를 버림과 전단을 놓침은 다른 무게의 사고다",
     "keywords": [
      "TP",
      "FP",
      "정밀도",
      "재현율",
      "F1"
     ],
     "links": [
      "softmax-and-mnist-classification.html",
      "fine-tuning-and-transfer-learning.html",
      "output-format-and-metrics.html"
     ]
    },
    {
     "file": "fine-tuning-and-transfer-learning.html",
     "concept": "파인튜닝·전이학습",
     "one_line": "사전학습된 모델의 앞쪽 눈은 얼리고 마지막 판단 층만 다시 학습시킨다",
     "practice": "사진 몇백 장뿐인 프로젝트에서 사전학습 가중치를 불러와 밑바닥 학습과 정확도를 비교한다",
     "analogy": "선·모서리 보는 눈은 두고 판단 기준만 조정",
     "keywords": [
      "파인튜닝",
      "전이학습",
      "ResNet18",
      "freeze",
      "사전학습"
     ],
     "links": [
      "confusion-matrix-and-metrics.html",
      "why-gpu-and-colab-cli.html"
     ]
    },
    {
     "file": "why-gpu-and-colab-cli.html",
     "concept": "GPU 병렬 계산",
     "one_line": "GPU는 단순 코어 수천 개로 행렬 곱셈을 동시에 처리해 학습을 크게 빠르게 한다",
     "practice": "학습이 몇 시간째 안 끝날 때 코드 대신 torch.cuda.is_available()부터 확인한다",
     "analogy": "빠른 소수 코어(CPU) vs 단순 코어 수천 개",
     "keywords": [
      "GPU",
      "CPU",
      "Colab CLI",
      "파라미터 규모",
      "병렬 계산"
     ],
     "links": [
      "fine-tuning-and-transfer-learning.html",
      "how-cnn-broke-the-depth-wall.html"
     ]
    }
   ],
   "name": "머신러닝 기초"
  },
  "llm-theory": {
   "sub": "llm-theory",
   "role": "챗봇 답변의 비용·한계·능력을 트랜스포머 구조로 설명",
   "scenario": "80쪽짜리 문서를 통째로 AI에 붙였더니 중간 조항이 뭉개지는 경험을 하고, 그 원인을 어텐션 계산이 토큰 수의 제곱에 비례해 늘어나는 구조와 Lost in the Middle 연구로 되짚어 설명한 사례다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "깊이의 벽 돌파",
      "posts": [
       "how-cnn-broke-the-depth-wall.html"
      ]
     },
     {
      "id": "n2",
      "label": "순서의 벽 돌파",
      "posts": [
       "how-language-broke-the-order-wall.html"
      ]
     },
     {
      "id": "n3",
      "label": "트랜스포머 탄생",
      "posts": [
       "birth-of-the-transformer.html"
      ]
     },
     {
      "id": "n4",
      "label": "사전학습·스케일링",
      "posts": [
       "pretraining-and-scaling-laws.html"
      ]
     },
     {
      "id": "n5",
      "label": "정렬 기법",
      "posts": [
       "what-is-alignment-sft-rlhf-dpo.html"
      ]
     },
     {
      "id": "n6",
      "label": "언어 밖으로 확장",
      "posts": [
       "transformers-beyond-language.html"
      ]
     },
     {
      "id": "n7",
      "label": "토큰·컨텍스트 비용",
      "posts": [
       "tokens-and-context-window-cost.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n3",
      "지름길 물려줘"
     ],
     [
      "n2",
      "n3",
      "합류해"
     ],
     [
      "n3",
      "n4",
      "키워봐"
     ],
     [
      "n4",
      "n5",
      "말귀 맞춰"
     ],
     [
      "n5",
      "n6",
      "밖으로 퍼져"
     ],
     [
      "n6",
      "n7",
      "비용으로 남아"
     ]
    ]
   },
   "posts": [
    {
     "file": "how-cnn-broke-the-depth-wall.html",
     "concept": "CNN·ResNet 지름길",
     "one_line": "층을 깊게 쌓으면 학습 신호가 사라지는 문제를 skip connection으로 뚫었다",
     "practice": "새 모델 이름을 만날 때 몇 층을 어떤 지름길 구조로 쌓았는지부터 가늠한다",
     "analogy": "신호가 깎이지 않고 흐르는 뒷길을 놓은 것",
     "keywords": [
      "CNN",
      "ResNet",
      "vanishing gradient",
      "skip connection",
      "AlexNet"
     ],
     "links": [
      "why-gpu-and-colab-cli.html",
      "how-language-broke-the-order-wall.html"
     ]
    },
    {
     "file": "how-language-broke-the-order-wall.html",
     "concept": "RNN과 어텐션",
     "one_line": "문장을 벡터 하나로 압축하던 고정벡터 병목을 attention이 되돌아보기로 깼다",
     "practice": "긴 문장 번역·요약 품질이 떨어질 때 고정벡터 병목이 역사적 원인인지 가늠한다",
     "analogy": "3분 연설을 한 문장으로만 요약해 전달하라는 요구",
     "keywords": [
      "word2vec",
      "RNN",
      "LSTM",
      "seq2seq",
      "attention"
     ],
     "links": [
      "how-cnn-broke-the-depth-wall.html",
      "birth-of-the-transformer.html"
     ]
    },
    {
     "file": "birth-of-the-transformer.html",
     "concept": "Q/K/V 어텐션",
     "one_line": "Query·Key·Value로 모든 토큰이 서로를 동시에 참고해 병렬 계산한다",
     "practice": "긴 대화가 메모리를 많이 쓰는 이유를 동료에게 KV cache로 설명할 때 쓴다",
     "analogy": "질문 카드(Q)를 색인표(K)에 맞춰 책을 가져오는 것",
     "keywords": [
      "Query",
      "Key",
      "Value",
      "멀티헤드",
      "KV cache"
     ],
     "links": [
      "how-language-broke-the-order-wall.html",
      "pretraining-and-scaling-laws.html",
      "kv-cache-and-vram-budget.html"
     ]
    },
    {
     "file": "pretraining-and-scaling-laws.html",
     "concept": "스케일링 법칙",
     "one_line": "모델·데이터·계산량을 키우면 손실이 정해진 비율로 줄고 새 능력이 솟는다",
     "practice": "예시 두세 개만 주고 새 과제를 시킬 때 왜 재학습 없이 통하는지 설명한다",
     "analogy": "아무도 안 가르쳤는데 저절로 생긴 능력",
     "keywords": [
      "BERT",
      "GPT",
      "스케일링 법칙",
      "인컨텍스트 러닝",
      "퓨샷"
     ],
     "links": [
      "birth-of-the-transformer.html",
      "what-is-alignment-sft-rlhf-dpo.html"
     ]
    },
    {
     "file": "what-is-alignment-sft-rlhf-dpo.html",
     "concept": "정렬 기법",
     "one_line": "정렬은 새 지식을 안 심고, 아는 것을 어떻게 말할지 태도만 손질한다",
     "practice": "모델이 자신 있게 틀린 답을 낼 때 말투가 아니라 사전학습 시점 안의 지식인지 확인한다",
     "analogy": "질문에 질문 잇던 모델을 지시 따르게 고치는 것",
     "keywords": [
      "SFT",
      "RLHF",
      "DPO",
      "정렬",
      "보상 모델"
     ],
     "links": [
      "pretraining-and-scaling-laws.html",
      "transformers-beyond-language.html"
     ]
    },
    {
     "file": "transformers-beyond-language.html",
     "concept": "언어 밖 확장",
     "one_line": "무엇을 조각냈나와 무엇이 무엇을 참고하나, 두 질문이면 새 모델도 읽힌다",
     "practice": "새 AI 모델 뉴스가 뜰 때 조각(토큰)과 참고 방식부터 확인해 학습 부담을 줄인다",
     "analogy": "이미지를 16×16 패치로 잘라 단어처럼 취급",
     "keywords": [
      "ViT",
      "Whisper",
      "DiT",
      "패치",
      "토큰화"
     ],
     "links": [
      "what-is-alignment-sft-rlhf-dpo.html",
      "tokens-and-context-window-cost.html"
     ]
    },
    {
     "file": "tokens-and-context-window-cost.html",
     "concept": "토큰·컨텍스트 비용",
     "one_line": "토큰 수가 두 배면 어텐션 계산은 네 배 가까이 늘고, 중요 정보는 중간에서 묻힌다",
     "practice": "AI 요금이 예상보다 많이 나오면 입력·출력·호출 수 중 어디가 병목인지 짚는다",
     "analogy": "큰 작업대 생겼다고 품질이 저절로 오르지 않음",
     "keywords": [
      "토큰",
      "컨텍스트 창",
      "Lost in the Middle",
      "RAG",
      "KV cache"
     ],
     "links": [
      "transformers-beyond-language.html",
      "training-vs-inference-memory.html",
      "context-window-budget.html"
     ]
    }
   ],
   "name": "트랜스포머와 LLM 이론"
  },
  "local-llm": {
   "sub": "local-llm",
   "role": "회사 문서를 어디서 돌릴지 메모리·비용·통제권으로 결정",
   "scenario": "재무팀이 계약서 PDF를 AI로 처리하려 할 때, 민감한 문서는 로컬 Ollama로 돌리고 나머지는 API로 라우팅하는 하이브리드 결정문을 데이터·비용·주권 근거와 함께 작성한 실제 판단 과정이다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "학습·추론 구분",
      "posts": [
       "training-vs-inference-memory.html"
      ]
     },
     {
      "id": "n2",
      "label": "양자화로 압축",
      "posts": [
       "quantization-why-it-still-works.html"
      ]
     },
     {
      "id": "n3",
      "label": "KV캐시·VRAM 계산",
      "posts": [
       "kv-cache-and-vram-budget.html"
      ]
     },
     {
      "id": "n4",
      "label": "Ollama 실습",
      "posts": [
       "running-local-llm-with-ollama.html"
      ]
     },
     {
      "id": "n5",
      "label": "실행 경로 선택",
      "posts": [
       "three-ways-to-run-an-llm.html"
      ]
     },
     {
      "id": "n6",
      "label": "데이터·비용·통제권",
      "posts": [
       "where-does-your-data-stay.html",
       "cost-and-control-of-local-llm.html"
      ]
     },
     {
      "id": "n7",
      "label": "값과 위치 구분",
      "posts": [
       "value-vs-location-two-requests.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "압축해"
     ],
     [
      "n2",
      "n3",
      "메모리 재"
     ],
     [
      "n3",
      "n4",
      "직접 돌려"
     ],
     [
      "n4",
      "n5",
      "경로 골라"
     ],
     [
      "n5",
      "n6",
      "결정 내려"
     ],
     [
      "n6",
      "n7",
      "다음 문제로"
     ]
    ]
   },
   "posts": [
    {
     "file": "training-vs-inference-memory.html",
     "concept": "학습 vs 추론 메모리",
     "one_line": "학습은 파라미터당 18바이트, 추론은 2바이트대만 있으면 된다",
     "practice": "노트북에서 모델이 돌지 가늠할 때 파라미터 수 × 2바이트로 어림 계산한다",
     "analogy": "남이 수백만 달러 들인 숫자 뭉치를 읽기만 하는 것",
     "keywords": [
      "학습",
      "추론",
      "FP16",
      "옵티마이저",
      "그래디언트"
     ],
     "links": [
      "tokens-and-context-window-cost.html",
      "quantization-why-it-still-works.html"
     ]
    },
    {
     "file": "quantization-why-it-still-works.html",
     "concept": "양자화(Q4_K_M)",
     "one_line": "16비트 눈금을 4비트로 성기게 반올림해도 1등 토큰은 잘 안 바뀐다",
     "practice": "받으려는 모델 파일이 여러 버전일 때 Q4_K_M 같은 파일명 표기를 읽고 고른다",
     "analogy": "6만 5천 눈금짜리 자를 16눈금짜리 자로 바꾸는 것",
     "keywords": [
      "양자화",
      "Q4_K_M",
      "K-quant",
      "GGUF",
      "Perplexity"
     ],
     "links": [
      "training-vs-inference-memory.html",
      "kv-cache-and-vram-budget.html"
     ]
    },
    {
     "file": "kv-cache-and-vram-budget.html",
     "concept": "KV 캐시·VRAM 예산",
     "one_line": "필요 메모리는 가중치+KV캐시+런타임 오버헤드 세 항의 합이다",
     "practice": "8GB 카드에 4.6GB 모델이 들어간다고 계산했다가 컨텍스트를 늘리면 자리가 모자란다",
     "analogy": "가중치 파일 크기만 보고 계산하면 반드시 틀리는 함정",
     "keywords": [
      "KV cache",
      "VRAM",
      "GQA",
      "MoE",
      "컨텍스트 길이"
     ],
     "links": [
      "quantization-why-it-still-works.html",
      "running-local-llm-with-ollama.html"
     ]
    },
    {
     "file": "running-local-llm-with-ollama.html",
     "concept": "Ollama 실습",
     "one_line": "작은 모델부터 크기 사다리를 올라가며 같은 질문 네 종류로 직접 재본다",
     "practice": "회사 문서를 AI에 넣기 꺼려질 때 ollama ps로 GPU에 온전히 올라갔는지 확인한다",
     "analogy": "들어간다는 계산과 실제 쓸 만한 속도는 다른 문제",
     "keywords": [
      "Ollama",
      "ollama ps",
      "eval rate",
      "양자화 비교",
      "-cloud"
     ],
     "links": [
      "kv-cache-and-vram-budget.html",
      "three-ways-to-run-an-llm.html"
     ]
    },
    {
     "file": "three-ways-to-run-an-llm.html",
     "concept": "세 갈래 실행 경로",
     "one_line": "AI 실행 경로는 공개 클라우드·관리형 프라이빗·로컬 세 갈래다",
     "practice": "규제 산업 프로젝트에서 로컬이냐 API냐로만 좁히지 않고 조직 전용 배포를 검토한다",
     "analogy": "프런티어 추격 기사와 내 노트북 성능은 두 겹 격차",
     "keywords": [
      "공개 클라우드",
      "관리형 프라이빗",
      "로컬",
      "품질 격차",
      "Ollama Cloud"
     ],
     "links": [
      "running-local-llm-with-ollama.html",
      "where-does-your-data-stay.html"
     ]
    },
    {
     "file": "where-does-your-data-stay.html",
     "concept": "데이터 보관 vs 학습 사용",
     "one_line": "학습에 안 쓴다는 약속과 남지 않는다는 약속은 따로 설정되는 별개 장치다",
     "practice": "회사에 AI 도구를 들일 때 로그 보관·처리 리전·삭제 가능 여부를 문서로 확인한다",
     "analogy": "제로 보관도 문자 그대로 0은 아니고 예외가 있다",
     "keywords": [
      "ZDR",
      "로그 보관",
      "처리 리전",
      "하위 처리자",
      "DPA"
     ],
     "links": [
      "three-ways-to-run-an-llm.html",
      "cost-and-control-of-local-llm.html"
     ]
    },
    {
     "file": "cost-and-control-of-local-llm.html",
     "concept": "손익분기·통제권",
     "one_line": "로컬 비용은 전기요금과 담당자 시간에 섞여 있어 청구서가 없다고 공짜가 아니다",
     "practice": "로컬 모델로 바꾸면 싸진다고 회의에서 주장할 때 남의 손익분기 숫자 대신 내 전력·가동률로 다시 계산한다",
     "analogy": "정리된 외부 계약이 허술한 내부 운영보다 설명하기 쉽다",
     "keywords": [
      "손익분기",
      "통제권",
      "회귀 테스트",
      "버전 고정",
      "결정문"
     ],
     "links": [
      "where-does-your-data-stay.html",
      "value-vs-location-two-requests.html"
     ]
    },
    {
     "file": "value-vs-location-two-requests.html",
     "concept": "값 뽑기 vs 위치 짚기",
     "one_line": "문서 읽기 요청은 값을 뽑는 일과 위치를 짚는 일이 섞여 있고 검증법이 다르다",
     "practice": "계약서에서 뽑은 금액이 부가세 칸과 뒤바뀌었을 때 검산 규칙이 코드에 있는지 확인한다",
     "analogy": "금액은 검산으로, 위치는 정답 영역과의 겹침으로 확인",
     "keywords": [
      "OCR",
      "값 추출",
      "위치 검출",
      "검산",
      "IoU"
     ],
     "links": [
      "cost-and-control-of-local-llm.html",
      "why-cant-ai-read-this-pdf.html"
     ]
    }
   ],
   "name": "로컬 LLM과 경량화"
  },
  "vision-ocr": {
   "sub": "vision-ocr",
   "role": "문서와 사진에서 글자·위치·경계를 꺼내 업무 판단에 쓴다",
   "scenario": "계약서 스캔본에서 금액을 표로 뽑아내거나 창고 사진에서 파렛트 개수를 세는 것처럼, OCR·탐지·분할·VLM으로 원본에서 근거를 찾아 업무 판단에 쓴다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "문서/사진 판별",
      "posts": [
       "why-cant-ai-read-this-pdf.html"
      ]
     },
     {
      "id": "n2",
      "label": "OCR 조립라인",
      "posts": [
       "ocr-assembly-line-and-error-propagation.html"
      ]
     },
     {
      "id": "n3",
      "label": "위치 탐지",
      "posts": [
       "object-detection-and-iou.html"
      ]
     },
     {
      "id": "n4",
      "label": "픽셀 분할",
      "posts": [
       "segmentation-and-sam.html"
      ]
     },
     {
      "id": "n5",
      "label": "VLM 해석",
      "posts": [
       "vision-language-models.html"
      ]
     },
     {
      "id": "n6",
      "label": "도구 상담·실습",
      "posts": [
       "choosing-ai-tools-and-yolo-practice.html"
      ]
     },
     {
      "id": "n7",
      "label": "결정은 사람 몫",
      "posts": [
       "outsourced-labor-kept-decisions.html",
       "blank-slots-model-decides.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "글자면 OCR"
     ],
     [
      "n1",
      "n3",
      "위치면 탐지"
     ],
     [
      "n3",
      "n4",
      "경계 필요시"
     ],
     [
      "n1",
      "n5",
      "해석 필요시"
     ],
     [
      "n2",
      "n6",
      "결과 비교"
     ],
     [
      "n4",
      "n6",
      "결과 비교"
     ],
     [
      "n5",
      "n6",
      "결과 비교"
     ],
     [
      "n6",
      "n7",
      "근거로 결정"
     ]
    ]
   },
   "posts": [
    {
     "file": "why-cant-ai-read-this-pdf.html",
     "concept": "OCR과 텍스트 PDF 구분",
     "one_line": "PDF는 텍스트 있는 것과 스캔 이미지뿐인 것 두 종류다",
     "practice": "AI가 PDF 내용 없다고 할 때, 텍스트가 마우스로 선택되는지 먼저 확인한다",
     "analogy": "",
     "keywords": [
      "OCR",
      "텍스트 레이어",
      "스캔본",
      "Tesseract",
      "PaddleOCR"
     ],
     "links": [
      "value-vs-location-two-requests.html",
      "ocr-assembly-line-and-error-propagation.html"
     ]
    },
    {
     "file": "ocr-assembly-line-and-error-propagation.html",
     "concept": "OCR 조립 라인·오류 전파",
     "one_line": "전처리→검출→인식→레이아웃 네 정거장 오류가 뒤로 번진다",
     "practice": "OCR 숫자가 이상할 때 전처리 이미지부터 단계별로 확인한다",
     "analogy": "자동차 공장 조립 라인",
     "keywords": [
      "기울기 보정",
      "이진화",
      "CRNN",
      "오류 전파",
      "레이아웃 분석"
     ],
     "links": [
      "why-cant-ai-read-this-pdf.html",
      "object-detection-and-iou.html"
     ]
    },
    {
     "file": "object-detection-and-iou.html",
     "concept": "객체 탐지와 IoU",
     "one_line": "탐지는 label·box·score 목록이고 IoU로 겹침을 잰다",
     "practice": "화재 감지처럼 놓치면 위험한 업무는 신뢰도 문턱을 낮게 잡는다",
     "analogy": "",
     "keywords": [
      "YOLO",
      "IoU",
      "신뢰도 점수",
      "신뢰도 임계값",
      "mAP"
     ],
     "links": [
      "ocr-assembly-line-and-error-propagation.html",
      "segmentation-and-sam.html"
     ]
    },
    {
     "file": "segmentation-and-sam.html",
     "concept": "이미지 분할과 SAM",
     "one_line": "분할은 픽셀마다 라벨 붙여 넓이·불규칙 형태·겹침을 답한다",
     "practice": "도장 손상 면적으로 보험금 산정할 때 경계 오차가 한 방향으로 쏠렸는지 본다",
     "analogy": "",
     "keywords": [
      "시맨틱 분할",
      "인스턴스 분할",
      "파놉틱 분할",
      "SAM",
      "경계 정의서"
     ],
     "links": [
      "object-detection-and-iou.html",
      "vision-language-models.html"
     ]
    },
    {
     "file": "vision-language-models.html",
     "concept": "VLM(시각-언어 모델)",
     "one_line": "이미지를 특징 벡터로 바꿔 언어 모델과 연결해 문맥까지 해석한다",
     "practice": "계약서의 '발주자'가 갑인지처럼 문맥 해석이 필요할 때 VLM을 쓴다",
     "analogy": "통역기·곁눈질·요약 비서",
     "keywords": [
      "비전 인코더",
      "Projector",
      "Cross-attention",
      "Q-Former",
      "PaddleOCR-VL"
     ],
     "links": [
      "segmentation-and-sam.html",
      "choosing-ai-tools-and-yolo-practice.html"
     ]
    },
    {
     "file": "choosing-ai-tools-and-yolo-practice.html",
     "concept": "도구 상담·YOLO 실습",
     "one_line": "AI에게 추천받기 전에 업무 조건을 먼저 질문하게 만든다",
     "practice": "새 AI 도구를 고를 때 이름 대신 입력·출력·실패 비용을 먼저 답한다",
     "analogy": "",
     "keywords": [
      "Flipped Interaction Pattern",
      "아첨 편향",
      "신뢰도 임계값",
      "탐지·분할·포즈",
      "라이선스"
     ],
     "links": [
      "vision-language-models.html",
      "outsourced-labor-kept-decisions.html"
     ]
    },
    {
     "file": "outsourced-labor-kept-decisions.html",
     "concept": "노동은 위임, 결정은 사람",
     "one_line": "읽고 보는 노동은 넘겨도 결과를 믿을지는 사람이 정한다",
     "practice": "도구 여섯 종을 표로 비교해 자료형·검증법·실패 유형을 기록해 둔다",
     "analogy": "",
     "keywords": [
      "원본 해시",
      "모델 버전 기록",
      "UNCLEAR 표시",
      "감사 추적",
      "오류 전파"
     ],
     "links": [
      "choosing-ai-tools-and-yolo-practice.html",
      "blank-slots-model-decides.html"
     ]
    },
    {
     "file": "blank-slots-model-decides.html",
     "concept": "빈 칸은 모델이 채움",
     "one_line": "프롬프트에 안 적은 칸은 학습 데이터의 흔한 값으로 모델이 채운다",
     "practice": "생성 결과가 별로일 때 모델 탓 전에 어떤 칸이 비었는지 점검한다",
     "analogy": "사진작가가 셔터 누르기 전 정하는 여섯 가지",
     "keywords": [
      "프롬프트 빈 칸",
      "시드 고정",
      "여섯 칸",
      "이미지 생성",
      "검산 불가"
     ],
     "links": [
      "outsourced-labor-kept-decisions.html",
      "gan-to-diffusion-models.html"
     ]
    }
   ],
   "name": "비전과 문서 인식"
  },
  "image-video-gen": {
   "sub": "image-video-gen",
   "role": "프롬프트로 없던 이미지·영상을 만들어 실무 자료로 쓴다",
   "scenario": "발표 자료 표지가 비어 있는데 회사 사진첩엔 쓸 게 없을 때, 여섯 칸을 채운 프롬프트로 공장 노동자 사진을 직접 만들어 쓴다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "GAN·확산 등장",
      "posts": [
       "gan-to-diffusion-models.html"
      ]
     },
     {
      "id": "n2",
      "label": "잠재 확산·증류",
      "posts": [
       "latent-diffusion-and-distillation.html"
      ]
     },
     {
      "id": "n3",
      "label": "프롬프트 여섯칸",
      "posts": [
       "writing-image-prompts.html"
      ]
     },
     {
      "id": "n4",
      "label": "코드로 자동화",
      "posts": [
       "automating-image-generation.html"
      ]
     },
     {
      "id": "n5",
      "label": "라이선스 확인",
      "posts": [
       "choosing-image-generation-tools.html"
      ]
     },
     {
      "id": "n6",
      "label": "영상으로 확장",
      "posts": [
       "video-generation-and-empty-slots.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "가볍게 만듦"
     ],
     [
      "n2",
      "n3",
      "직접 써보기"
     ],
     [
      "n3",
      "n4",
      "코드로 반복"
     ],
     [
      "n4",
      "n5",
      "쓰기 전 확인"
     ],
     [
      "n5",
      "n6",
      "영상으로 확장"
     ]
    ]
   },
   "posts": [
    {
     "file": "gan-to-diffusion-models.html",
     "concept": "GAN에서 확산 모델로",
     "one_line": "그럴듯함을 못 채점해 GAN은 대결로, 확산은 잡음 맞히기로 풀었다",
     "practice": "생성 코드가 프롬프트를 무시할 때 모델이 GAN 계열인지 확산 계열인지 먼저 본다",
     "analogy": "위조범과 감정사",
     "keywords": [
      "GAN",
      "모드 붕괴",
      "확산 모델",
      "DDPM",
      "CLIP"
     ],
     "links": [
      "blank-slots-model-decides.html",
      "latent-diffusion-and-distillation.html"
     ]
    },
    {
     "file": "latent-diffusion-and-distillation.html",
     "concept": "잠재 확산과 증류",
     "one_line": "압축된 잠재 공간에서 확산을 돌려 개인 컴퓨터로 내려왔다",
     "practice": "증류 모델 코드에서 guidance_scale을 임의로 올리지 않고 0으로 둔다",
     "analogy": "",
     "keywords": [
      "잠재 공간",
      "오토인코더",
      "Stable Diffusion",
      "DiT",
      "증류"
     ],
     "links": [
      "gan-to-diffusion-models.html",
      "writing-image-prompts.html"
     ]
    },
    {
     "file": "writing-image-prompts.html",
     "concept": "이미지 프롬프트 여섯 칸",
     "one_line": "피사체·동작·카메라·조명·환경·스타일 여섯 칸을 문장으로 채운다",
     "practice": "결과가 안 좋을 때 모델을 바꾸기 전에 빈 칸부터 한 칸씩 채워 다시 본다",
     "analogy": "",
     "keywords": [
      "여섯 칸",
      "네거티브 프롬프트",
      "시드 고정",
      "긍정형 표현",
      "인페인팅"
     ],
     "links": [
      "latent-diffusion-and-distillation.html",
      "automating-image-generation.html"
     ]
    },
    {
     "file": "automating-image-generation.html",
     "concept": "이미지 생성 자동화",
     "one_line": "프롬프트를 코드로 모델에 보내 여러 장을 한꺼번에 받는다",
     "practice": "상품 백 개 썸네일 만들 때 파이프라인을 반복문 밖에서 한 번만 올린다",
     "analogy": "",
     "keywords": [
      "API",
      "Colab GPU",
      "diffusers",
      "guidance_scale",
      "시드 재현"
     ],
     "links": [
      "writing-image-prompts.html",
      "choosing-image-generation-tools.html"
     ]
    },
    {
     "file": "choosing-image-generation-tools.html",
     "concept": "라이선스·ControlNet",
     "one_line": "모델 라이선스·서비스 약관·저작권법 세 층을 따로 확인해야 한다",
     "practice": "회사 프로젝트에 쓸 모델은 배포 페이지 라이선스 배지부터 확인한다",
     "analogy": "",
     "keywords": [
      "아파치 2.0",
      "비상업 라이선스",
      "ControlNet",
      "OpenPose",
      "서비스 약관"
     ],
     "links": [
      "automating-image-generation.html",
      "video-generation-and-empty-slots.html"
     ]
    },
    {
     "file": "video-generation-and-empty-slots.html",
     "concept": "영상 프롬프트의 빈 칸",
     "one_line": "카메라·동작 빈 칸도 모델이 정하니 고정과 끝점을 직접 적는다",
     "practice": "화면이 이유 없이 흔들릴 때 카메라 움직임 칸이 비었는지 확인한다",
     "analogy": "",
     "keywords": [
      "카메라 고정",
      "동작 끝점",
      "8~10초 토막",
      "ControlNet Pose",
      "이미지투비디오"
     ],
     "links": [
      "choosing-image-generation-tools.html",
      "why-multimodal-one-model.html"
     ]
    }
   ],
   "name": "이미지·영상 생성"
  },
  "multimodal-voice": {
   "sub": "multimodal-voice",
   "role": "여러 입력을 합칠지 나눌지 정해 업무 판단·회의록에 쓴다",
   "scenario": "보험 심사에서 경위서·파손 사진·상담 녹음을 합쳐 판단할지 나눠 검증할지 정하는 것처럼, 음성·이미지를 업무에 끌어들인다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "합칠지 나눌지",
      "posts": [
       "why-multimodal-one-model.html"
      ]
     },
     {
      "id": "n2",
      "label": "CLIP 정렬",
      "posts": [
       "clip-and-vision-language-models.html"
      ]
     },
     {
      "id": "n3",
      "label": "소리를 글자로",
      "posts": [
       "speech-to-text-history.html"
      ]
     },
     {
      "id": "n4",
      "label": "로컬 위스퍼 고르기",
      "posts": [
       "choosing-a-local-whisper.html"
      ]
     },
     {
      "id": "n5",
      "label": "옴니·추론엔진",
      "posts": [
       "omni-models-and-inference-engines.html"
      ]
     },
     {
      "id": "n6",
      "label": "글자를 소리로",
      "posts": [
       "choosing-a-voice-synthesis-tool.html"
      ]
     },
     {
      "id": "n7",
      "label": "복제 책임",
      "posts": [
       "voice-cloning-and-responsible-ai.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "정렬 사례"
     ],
     [
      "n1",
      "n3",
      "분리 사례"
     ],
     [
      "n3",
      "n4",
      "크기 선택"
     ],
     [
      "n4",
      "n5",
      "통째로 받기"
     ],
     [
      "n5",
      "n6",
      "반대로 합성"
     ],
     [
      "n6",
      "n7",
      "복제하면 책임"
     ]
    ]
   },
   "posts": [
    {
     "file": "why-multimodal-one-model.html",
     "concept": "모달리티와 합치기/나누기",
     "one_line": "글·이미지·소리를 합칠지 나눌지 네 질문으로 정한다",
     "practice": "보험 심사에서 검증이 중요하면 소리를 먼저 글자로 옮겨 판단을 나눈다",
     "analogy": "웃으며 vs 눈 피하며 하는 '괜찮아요'",
     "keywords": [
      "모달리티",
      "합치기/나누기",
      "검증 가능성",
      "전문 도구",
      "응답 지연"
     ],
     "links": [
      "video-generation-and-empty-slots.html",
      "clip-and-vision-language-models.html"
     ]
    },
    {
     "file": "clip-and-vision-language-models.html",
     "concept": "CLIP과 VLM 세 구조",
     "one_line": "CLIP은 이미지와 문장을 같은 좌표 공간에 정렬해 거리로 비교한다",
     "practice": "상품 사진 설명 시킬 때 필요한 항목을 먼저 적고 하나씩 물어본다",
     "analogy": "",
     "keywords": [
      "대조 학습",
      "정렬",
      "연결형",
      "공유임베딩형",
      "네이티브멀티모달형"
     ],
     "links": [
      "why-multimodal-one-model.html",
      "speech-to-text-history.html"
     ]
    },
    {
     "file": "speech-to-text-history.html",
     "concept": "STT 반백년의 계보",
     "one_line": "발음사전 조립 구조에서 정답 없이 배우는 방식까지 STT가 바뀌었다",
     "practice": "받아쓰기 오타가 많을 때 모델보다 녹음 마이크 환경부터 의심한다",
     "analogy": "",
     "keywords": [
      "HMM-GMM",
      "CTC",
      "wav2vec 2.0",
      "Whisper",
      "약지도학습"
     ],
     "links": [
      "clip-and-vision-language-models.html",
      "choosing-a-local-whisper.html"
     ]
    },
    {
     "file": "choosing-a-local-whisper.html",
     "concept": "로컬 Whisper 고르기",
     "one_line": "내 하드웨어에서 정확도와 속도가 맞는 크기와 포맷을 고른다",
     "practice": "애플 실리콘에서 받아쓰기가 느리면 GGUF 대신 MLX 포맷을 찾는다",
     "analogy": "",
     "keywords": [
      "tiny~large-v3",
      "CER",
      "GGUF",
      "MLX",
      "한국어 파인튜닝"
     ],
     "links": [
      "speech-to-text-history.html",
      "omni-models-and-inference-engines.html"
     ]
    },
    {
     "file": "omni-models-and-inference-engines.html",
     "concept": "옴니 모델과 추론 엔진",
     "one_line": "한 모델이 글·소리·이미지·영상 다 받되 실제 입력은 도구가 정한다",
     "practice": "녹음 내용을 못 맞히면 로컬 도구가 소리를 모델까지 안 보낸 것이다",
     "analogy": "",
     "keywords": [
      "옴니 모델",
      "Gemma",
      "추론 엔진",
      "vLLM",
      "중간 산출물"
     ],
     "links": [
      "choosing-a-local-whisper.html",
      "choosing-a-voice-synthesis-tool.html"
     ]
    },
    {
     "file": "choosing-a-voice-synthesis-tool.html",
     "concept": "목소리 합성기 고르기",
     "one_line": "한국어 품질·실행 환경과 함께 라이선스가 상업 사용 허락하는지 본다",
     "practice": "사내 문서 읽어줄 TTS 고를 때 코드와 가중치 라이선스를 따로 확인한다",
     "analogy": "",
     "keywords": [
      "TTS",
      "supertonic",
      "Fish Audio S2 Pro",
      "목소리 복제",
      "가중치 라이선스"
     ],
     "links": [
      "omni-models-and-inference-engines.html",
      "voice-cloning-and-responsible-ai.html"
     ]
    },
    {
     "file": "voice-cloning-and-responsible-ai.html",
     "concept": "복제 책임·요약 세탁",
     "one_line": "실제로 걸리는 건 법이 아니라 모델 라이선스와 목소리 주인의 동의다",
     "practice": "회의록 공유 전에 날짜·숫자를 받아쓰기 원문과 대조해 지어낸 게 없는지 본다",
     "analogy": "",
     "keywords": [
      "표시 의무",
      "목소리 동의",
      "요약 세탁",
      "오류율",
      "잡음 억제"
     ],
     "links": [
      "choosing-a-voice-synthesis-tool.html",
      "why-photos-lose-distance.html"
     ]
    }
   ],
   "name": "멀티모달과 음성"
  },
  "three-d-reconstruction": {
   "sub": "three-d-reconstruction",
   "role": "사진 여러 장을 돌려 볼 수 있는 3D 화면으로 바꿔주는 역할",
   "scenario": "중고 거래 물건이나 부동산 매물 사진을 아무리 더 찍어도 안 보이던 공간감을, 폰 영상 15~20초로 만든 3D 스캔 화면 하나로 대신하는 장면.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "사진 촬영",
      "posts": [
       "why-photos-lose-distance.html"
      ]
     },
     {
      "id": "n2",
      "label": "그릇 고르기",
      "posts": [
       "four-containers-for-3d-space.html"
      ]
     },
     {
      "id": "n3",
      "label": "장면 복원",
      "posts": [
       "birth-of-nerf-and-gaussian-splatting.html",
       "recovering-depth-from-photos.html",
       "thirty-years-of-3d-reconstruction.html"
      ]
     },
     {
      "id": "n4",
      "label": "알갱이로 변환",
      "posts": [
       "turning-points-into-splats.html"
      ]
     },
     {
      "id": "n5",
      "label": "압축 후 게시",
      "posts": [
       "shrinking-splat-files-for-the-web.html"
      ]
     },
     {
      "id": "n6",
      "label": "품질 판단",
      "posts": [
       "judging-and-fixing-a-3d-scan.html"
      ]
     },
     {
      "id": "n7",
      "label": "라이선스 확인",
      "posts": [
       "famous-is-not-the-same-as-usable.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "그릇 정하기"
     ],
     [
      "n2",
      "n3",
      "거리 복원"
     ],
     [
      "n3",
      "n4",
      "알갱이 변환"
     ],
     [
      "n4",
      "n5",
      "압축 배포"
     ],
     [
      "n5",
      "n6",
      "품질 점검"
     ],
     [
      "n6",
      "n7",
      "쓸 수 있나 확인"
     ]
    ]
   },
   "posts": [
    {
     "file": "why-photos-lose-distance.html",
     "concept": "거리 정보 손실",
     "one_line": "사진은 칸마다 RGB 세 숫자만 남겨 3차원이 눌리며 거리가 사라진다",
     "practice": "중고 물건 사진을 여러 장 더 찍어달라는 요청이 반복될 때 3D 스캔으로 대체한다",
     "analogy": "",
     "keywords": [
      "시차",
      "디지털트윈",
      "코랩",
      "정적호스팅"
     ],
     "links": []
    },
    {
     "file": "four-containers-for-3d-space.html",
     "concept": "3D 담는 네 그릇",
     "one_line": "메시·포인트클라우드·복셀·스플랫, 담는 방식마다 잘하는 일이 다르다",
     "practice": "에이전트에게 3D 변환을 시킬 때 메시·스플랫처럼 그릇 이름을 정확히 지정한다",
     "analogy": "",
     "keywords": [
      "메시",
      "포인트클라우드",
      "복셀",
      "가우시안스플랫",
      "새시점합성"
     ],
     "links": [
      "blank-slots-model-decides.html"
     ]
    },
    {
     "file": "birth-of-nerf-and-gaussian-splatting.html",
     "concept": "NeRF와 스플래팅",
     "one_line": "NeRF는 신경망에 묻고 스플래팅은 알갱이를 화면에 찍어 발라 그린다",
     "practice": "매물 화면을 만들 때 화질 우선이면 NeRF 계열을, 웹 실시간이면 스플래팅을 쓴다",
     "analogy": "붓에 물감 묻혀 벽에 튀기는 동작(splat)",
     "keywords": [
      "NeRF",
      "가우시안스플래팅",
      "구면조화",
      "radiance field"
     ],
     "links": []
    },
    {
     "file": "recovering-depth-from-photos.html",
     "concept": "시차와 깊이 추정",
     "one_line": "걸어 다니며 찍은 사진들이 어긋난 정도(시차)로 거리를 되찾는다",
     "practice": "3D 스캔용 사진을 찍을 때 제자리 회전 대신 15~20초 걸어 다니며 촬영한다",
     "analogy": "차창 밖 가로수는 휙휙, 먼 산은 안 움직이는 것",
     "keywords": [
      "시차",
      "단안깊이추정",
      "역깊이",
      "MapAnything",
      "SfM"
     ],
     "links": [
      "quantization-why-it-still-works.html"
     ]
    },
    {
     "file": "turning-points-into-splats.html",
     "concept": "점을 알갱이로 변환",
     "one_line": "점 파일의 숫자 6개로 알갱이 하나에 필요한 62칸을 채우는 계산이다",
     "practice": "스캔 결과가 뿌옇거나 구멍이 뚫릴 때 되돌리기 계산과 크기 기준을 점검한다",
     "analogy": "",
     "keywords": [
      "구면조화",
      "시그모이드",
      "사원수",
      "알갱이크기"
     ],
     "links": []
    },
    {
     "file": "shrinking-splat-files-for-the-web.html",
     "concept": ".sog 파일 압축",
     "one_line": "자리·크기·회전·색을 이미지로 바꿔 사진 압축기로 파일을 14배 줄인다",
     "practice": "3D 결과가 100MB 넘어 업로드가 막힐 때 알갱이를 지우기 전에 .sog로 바꾼다",
     "analogy": "셀로판지 세 장, 겹치는 순서 다르면 색도 달라짐",
     "keywords": [
      ".sog",
      "알파블렌딩",
      "WebGL2",
      "양자화"
     ],
     "links": []
    },
    {
     "file": "thirty-years-of-3d-reconstruction.html",
     "concept": "3D 복원 계보",
     "one_line": "SfM·SLAM·복셀·피드포워드 네 갈래가 저마다 무언가를 내주고 문제를 풀었다",
     "practice": "새 3D 도구 이름을 만났을 때 무엇이 막혔고 무엇을 내줬는지 세 질문으로 분류한다",
     "analogy": "",
     "keywords": [
      "SfM",
      "SLAM",
      "COLMAP",
      "점유예측",
      "피드포워드"
     ],
     "links": [
      "birth-of-nerf-and-gaussian-splatting.html",
      "recovering-depth-from-photos.html"
     ]
    },
    {
     "file": "judging-and-fixing-a-3d-scan.html",
     "concept": "스캔 품질 판단",
     "one_line": "PSNR·SSIM·LPIPS 세 자로 화소 차이·형태·사람 인상을 따로 잰다",
     "practice": "결과에 검은 구멍이 남을 때 카메라가 그쪽을 지나갔는지부터 확인한다",
     "analogy": "",
     "keywords": [
      "PSNR",
      "SSIM",
      "LPIPS",
      "시차확보"
     ],
     "links": [
      "turning-points-into-splats.html",
      "recovering-depth-from-photos.html",
      "git-commit-concept.html"
     ]
    },
    {
     "file": "famous-is-not-the-same-as-usable.html",
     "concept": "라이선스와 유명세",
     "one_line": "별 2만 개 넘는 구현도 조건 문서에는 연구용으로만 쓰라고 적혀 있다",
     "practice": "회사 일에 3D 도구를 쓸 때 LICENSE 파일에서 commercial 문구부터 확인한다",
     "analogy": "",
     "keywords": [
      "비상업라이선스",
      "MIT",
      "Apache-2.0",
      "지역배제"
     ],
     "links": [
      "recovering-depth-from-photos.html",
      "choosing-image-generation-tools.html"
     ]
    }
   ],
   "name": "3D 복원과 스플래팅"
  },
  "science-ai": {
   "sub": "science-ai",
   "role": "챗봇 밖 단백질·기상·로봇 같은 실전 문제에 AI를 붙이는 역할",
   "scenario": "실험 후보가 수만 개라 막막할 때 세포 몇천 개만 미리 배운 모델에 보여줘, 실제로 실험할 후보를 수만 개에서 열 개로 줄이는 장면.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "새 분야 발견",
      "posts": [
       "same-week-different-fields.html"
      ]
     },
     {
      "id": "n2",
      "label": "기반모델로 답하기",
      "posts": [
       "foundation-models-for-tables.html",
       "from-sequence-to-structure.html"
      ]
     },
     {
      "id": "n3",
      "label": "확산으로 생성",
      "posts": [
       "designing-proteins-backwards.html",
       "new-molecules-new-crystals.html"
      ]
     },
     {
      "id": "n4",
      "label": "관계로 정교화",
      "posts": [
       "graphs-and-interatomic-forces.html",
       "learning-the-weather-instead-of-computing-it.html"
      ]
     },
     {
      "id": "n5",
      "label": "몸과 보상으로 확장",
      "posts": [
       "a-model-with-a-body.html",
       "rewards-where-grading-is-possible.html"
      ]
     },
     {
      "id": "n6",
      "label": "쓸 수 있나 확인",
      "posts": [
       "open-versus-usable-today.html"
      ]
     },
     {
      "id": "n7",
      "label": "도입 문턱 판단",
      "posts": [
       "knowing-where-not-to-go-is-also-a-map.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "이름으로 검색"
     ],
     [
      "n2",
      "n3",
      "생성으로 확장"
     ],
     [
      "n3",
      "n4",
      "관계로 정교화"
     ],
     [
      "n4",
      "n5",
      "몸으로 확장"
     ],
     [
      "n5",
      "n6",
      "쓸 수 있나 확인"
     ],
     [
      "n6",
      "n7",
      "문턱 판단"
     ]
    ]
   },
   "posts": [
    {
     "file": "same-week-different-fields.html",
     "concept": "챗봇 밖 AI 네 발상",
     "one_line": "단백질 설계·기상 예보·로봇 같은 챗봇 밖 AI는 네 가지 발상으로 묶인다",
     "practice": "새 AI 도구를 받을 때 설치·무료환경·라이선스·관리·속도 다섯 조건을 확인한다",
     "analogy": "",
     "keywords": [
      "기반모델",
      "확산",
      "그래프신경망",
      "검증가능한보상"
     ],
     "links": []
    },
    {
     "file": "foundation-models-for-tables.html",
     "concept": "표 기반모델",
     "one_line": "표를 통째로 맥락에 넣으면 학습 없이 한 번의 계산으로 답이 나온다",
     "practice": "표로 예측할 때 순진한 기준선과 나란히 재서 기반모델이 이기는지 확인한다",
     "analogy": "",
     "keywords": [
      "맥락내학습",
      "TabICL",
      "Chronos",
      "순진한기준선",
      "자료유출"
     ],
     "links": [
      "clip-and-vision-language-models.html",
      "how-cnn-broke-the-depth-wall.html"
     ]
    },
    {
     "file": "from-sequence-to-structure.html",
     "concept": "서열 기반모델",
     "one_line": "DNA·단백질은 글자가 늘어선 서열이라 언어모델 구조를 그대로 쓴다",
     "practice": "실험 후보가 수만 개라 막막할 때 세포 몇천 개만 보여줘 후보 순위를 받는다",
     "analogy": "",
     "keywords": [
      "Geneformer",
      "AlphaFold2",
      "pLDDT",
      "ColabFold"
     ],
     "links": []
    },
    {
     "file": "designing-proteins-backwards.html",
     "concept": "역방향 단백질 설계",
     "one_line": "잡음에서 뼈대를 얻고 그 위에 서열을 입혀 없던 단백질을 짓는다",
     "practice": "표적에 붙는 물질을 찾을 때 뼈대를 생성해 예측기로 걸러 후보를 줄인다",
     "analogy": "",
     "keywords": [
      "RFdiffusion",
      "ProteinMPNN",
      "역접힘",
      "검증가능한보상"
     ],
     "links": [
      "from-sequence-to-structure.html",
      "gan-to-diffusion-models.html",
      "voice-cloning-and-responsible-ai.html"
     ]
    },
    {
     "file": "new-molecules-new-crystals.html",
     "concept": "분자·결정 생성",
     "one_line": "창고에서 고르는 대신 조건에 맞는 새 분자·결정을 확산으로 그려낸다",
     "practice": "원하는 물질을 창고 목록에서 못 찾을 때 표적 모양에 맞춰 후보를 새로 생성한다",
     "analogy": "저울 위 무게는 안 바뀌지만 화살표는 돌리면 같이 돈다",
     "keywords": [
      "DiffSBDD",
      "MatterGen",
      "등변",
      "도킹"
     ],
     "links": []
    },
    {
     "file": "graphs-and-interatomic-forces.html",
     "concept": "그래프 신경망",
     "one_line": "점과 선으로 본 자료에서 이웃 정보로 상태를 고치면 정확도가 크게 오른다",
     "practice": "자료에 관계 정보가 있을 때 모델을 키우는 대신 그 관계를 그래프로 넣는다",
     "analogy": "",
     "keywords": [
      "메시지패싱",
      "CHGNet",
      "MACE",
      "구조이완"
     ],
     "links": []
    },
    {
     "file": "learning-the-weather-instead-of-computing-it.html",
     "concept": "기상 기반모델",
     "one_line": "유체 방정식을 안 풀고 관측 자료만 배워 열흘 예보를 1분에 낸다",
     "practice": "골짜기 서리 확률을 알아야 할 때 출발 조건을 흔들어 여러 번 돌려 답의 폭을 본다",
     "analogy": "",
     "keywords": [
      "GraphCast",
      "앙상블예보",
      "재분석자료",
      "PINN"
     ],
     "links": [
      "graphs-and-interatomic-forces.html"
     ]
    },
    {
     "file": "a-model-with-a-body.html",
     "concept": "VLA 로봇 모델",
     "one_line": "카메라 화면과 말을 넣으면 로봇 관절 각도를 바로 내놓는 모델이다",
     "practice": "로봇 품목이 바뀔 때 프로그램을 다시 짜는 대신 시범을 스무 번 다시 보여준다",
     "analogy": "",
     "keywords": [
      "VLA",
      "SmolVLA",
      "LeRobot",
      "세계모델"
     ],
     "links": [
      "gan-to-diffusion-models.html"
     ]
    },
    {
     "file": "rewards-where-grading-is-possible.html",
     "concept": "검증 가능한 보상",
     "one_line": "수학·코드처럼 기계가 답을 확인할 수 있는 곳에만 보상을 걸어 학습시킨다",
     "practice": "AI 채점 결과를 믿으려 할 때 같은 문제를 다시 풀어 최종 답이 매번 같은지 본다",
     "analogy": "",
     "keywords": [
      "GRPO",
      "DeepSeek-R1-Zero",
      "Lean",
      "강화학습"
     ],
     "links": [
      "smallest-learning-in-code.html"
     ]
    },
    {
     "file": "open-versus-usable-today.html",
     "concept": "라이선스 네 계단",
     "one_line": "코드·가중치·기반모델·학습자료 네 갈래가 각각 다른 조건으로 배포된다",
     "practice": "새 도구를 검토할 때 코드 배지만 보지 않고 가중치 페이지 조건까지 확인한다",
     "analogy": "",
     "keywords": [
      "가중치",
      "동의화면",
      "비상업",
      "학습자료"
     ],
     "links": [
      "famous-is-not-the-same-as-usable.html"
     ]
    },
    {
     "file": "knowing-where-not-to-go-is-also-a-map.html",
     "concept": "도입 문턱 네 가지",
     "one_line": "장비·절차·시간은 낮아지지만 판단할 사람 없는 문턱만은 안 낮아진다",
     "practice": "새 도구 결과를 못 믿겠을 때 장비·절차·시간 문제인지 판단자 부재인지 가른다",
     "analogy": "",
     "keywords": [
      "도입문턱",
      "기준선비교",
      "Evo2",
      "AlphaFold3"
     ],
     "links": [
      "famous-is-not-the-same-as-usable.html",
      "foundation-models-for-tables.html",
      "voice-cloning-and-responsible-ai.html"
     ]
    }
   ],
   "name": "과학·물리 AI"
  },
  "instruction-design": {
   "sub": "instruction-design",
   "role": "AI에게 시킬 일을 판정 가능한 계약으로 쓰는 역할",
   "scenario": "고객 문의 챗봇에 '배송일은 언제인가요?'라는 같은 질문을 놓고 지시를 A안(최소)·B안(제약 보강)·C안(형식 보강)으로 나눠, 근거 없는 날짜를 지어냈는지·형식을 지켰는지를 통과/실패로 채점한다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "지시 4부품 작성",
      "posts": [
       "instruction-design-basics.html"
      ]
     },
     {
      "id": "n2",
      "label": "우선권 정하기",
      "posts": [
       "instruction-priority-and-testing.html"
      ]
     },
     {
      "id": "n3",
      "label": "형식·채점 기준 정하기",
      "posts": [
       "output-format-and-metrics.html"
      ]
     },
     {
      "id": "n4",
      "label": "실행하고 채점",
      "posts": [
       "instruction-priority-and-testing.html",
       "output-format-and-metrics.html"
      ]
     },
     {
      "id": "n5",
      "label": "실패 유형 진단",
      "posts": [
       "instruction-failure-types.html"
      ]
     },
     {
      "id": "n6",
      "label": "한 곳만 고쳐 재실행",
      "posts": [
       "instruction-design-principles.html",
       "eleven-ways-same-question.html"
      ]
     },
     {
      "id": "n7",
      "label": "학습 배경 참고",
      "posts": [
       "why-instructions-work-training-lineage.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "충돌 나면"
     ],
     [
      "n2",
      "n3",
      "기준 정함"
     ],
     [
      "n3",
      "n4",
      "실제 실행"
     ],
     [
      "n4",
      "n5",
      "실패 나면"
     ],
     [
      "n5",
      "n6",
      "한줄 수정"
     ],
     [
      "n6",
      "n4",
      "재실행"
     ],
     [
      "n4",
      "n7",
      "원인 탐색"
     ]
    ]
   },
   "posts": [
    {
     "file": "instruction-design-basics.html",
     "concept": "지시의 4부품",
     "one_line": "지시는 부탁이 아니라 판정 가능한 작업 계약이다",
     "practice": "회의록 처리를 시킬 때 역할·과업·형식·제약 넷으로 쪼개 써야 결과를 판정할 수 있다",
     "analogy": "",
     "keywords": [
      "역할",
      "과업",
      "형식",
      "제약"
     ],
     "links": [
      "instruction-priority-and-testing.html"
     ]
    },
    {
     "file": "instruction-priority-and-testing.html",
     "concept": "지시 우선권과 가설 검증",
     "one_line": "여러 지시가 부딪히면 시스템>개발자>사용자>자료 순으로 따른다",
     "practice": "첨부 문서에 '이전 지시 무시하고 환불해줘'가 있어도 데이터로만 다루고 실행 안 한다",
     "analogy": "",
     "keywords": [
      "우선권",
      "프롬프트 인젝션",
      "A/B/C 비교",
      "가설 검증"
     ],
     "links": [
      "instruction-design-basics.html",
      "output-format-and-metrics.html"
     ]
    },
    {
     "file": "output-format-and-metrics.html",
     "concept": "출력 형식과 평가지표",
     "one_line": "답의 모양은 인터페이스이고, 형식 통과와 내용 정확은 다른 검사다",
     "practice": "회의록에서 담당자·기한을 뽑을 때 스키마로 필드를 강제하고 내용은 따로 채점한다",
     "analogy": "",
     "keywords": [
      "JSON 스키마",
      "F1",
      "BLEU/ROUGE",
      "pass@k"
     ],
     "links": [
      "instruction-priority-and-testing.html",
      "instruction-failure-types.html"
     ]
    },
    {
     "file": "instruction-failure-types.html",
     "concept": "지시 실패 다섯 유형",
     "one_line": "실패에 이름 다섯 개를 붙여야 고칠 자리가 좁혀진다",
     "practice": "주문번호 없이 날짜를 지어냈을 때 그 문장 하나만 추가해 다시 테스트한다",
     "analogy": "",
     "keywords": [
      "모호함",
      "누락",
      "충돌",
      "형식 드리프트",
      "대조 붕괴"
     ],
     "links": [
      "output-format-and-metrics.html",
      "instruction-design-principles.html"
     ]
    },
    {
     "file": "instruction-design-principles.html",
     "concept": "5단계 점검 순서",
     "one_line": "답이 어긋나면 과업→근거→제약→형식→채점 순서로 고칠 자리를 찾는다",
     "practice": "인사말이 붙는 형식 문제인데 역할부터 다시 쓰는 헛손질을 막아준다",
     "analogy": "",
     "keywords": [
      "점검 순서",
      "temperature",
      "top_p",
      "effort"
     ],
     "links": [
      "instruction-failure-types.html",
      "eleven-ways-same-question.html"
     ]
    },
    {
     "file": "eleven-ways-same-question.html",
     "concept": "프롬프트 기법 직접 재검증",
     "one_line": "로컬 모델로 같은 질문을 열한 가지 방법으로 돌려 기법의 이름값을 확인했다",
     "practice": "'소수점 쓰지 마라' 같은 금지 문장이 질문 해석 자체를 바꿔 오답을 냈다",
     "analogy": "",
     "keywords": [
      "zero-shot",
      "CoT",
      "temperature",
      "top_k",
      "qwen3.5:2b"
     ],
     "links": [
      "instruction-design-principles.html",
      "why-instructions-work-training-lineage.html"
     ]
    },
    {
     "file": "why-instructions-work-training-lineage.html",
     "concept": "지시 따르기의 훈련 계보",
     "one_line": "지시를 따르는 건 타고난 능력이 아니라 SFT·RLHF·DPO·GRPO로 학습된 습관이다",
     "practice": "모델·스냅샷을 바꾸면 예전 프롬프트가 안 통할 수 있어 대표 평가셋으로 다시 잰다",
     "analogy": "",
     "keywords": [
      "SFT",
      "RLHF",
      "DPO",
      "GRPO",
      "chat template"
     ],
     "links": [
      "eleven-ways-same-question.html",
      "context-window-budget.html"
     ]
    }
   ],
   "name": "지시 설계"
  },
  "context-engineering": {
   "sub": "context-engineering",
   "role": "AI 답에 무엇을 읽힐지 예산을 짜는 역할",
   "scenario": "반품 챗봇에 정책 문서·메모리·도구 목록·대화 이력을 함께 넣을 때, 컨텍스트 창이라는 유한한 적재함 안에서 무엇을 싣고 무엇을 뺄지 정한다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "적재함 예산 짜기",
      "posts": [
       "context-window-budget.html"
      ]
     },
     {
      "id": "n2",
      "label": "실제로 읽혔나 확인",
      "posts": [
       "lost-in-the-middle-and-context-rot.html"
      ]
     },
     {
      "id": "n3",
      "label": "실을 자료 고르기",
      "posts": [
       "context-strategy-and-rag.html"
      ]
     },
     {
      "id": "n4",
      "label": "조건 하나씩 검증",
      "posts": [
       "context-experiment-and-injection-defense.html"
      ]
     },
     {
      "id": "n5",
      "label": "비신뢰 입력 차단",
      "posts": [
       "context-experiment-and-injection-defense.html"
      ]
     },
     {
      "id": "n6",
      "label": "상시 파일·캐싱 설계",
      "posts": [
       "agents-md-and-cache-economics.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "실었다 믿으면"
     ],
     [
      "n2",
      "n3",
      "무엇 넣을지"
     ],
     [
      "n3",
      "n4",
      "선택 검증"
     ],
     [
      "n4",
      "n5",
      "자료 구분"
     ],
     [
      "n5",
      "n6",
      "상시 규칙화"
     ],
     [
      "n6",
      "n1",
      "예산 재점검"
     ]
    ]
   },
   "posts": [
    {
     "file": "context-window-budget.html",
     "concept": "컨텍스트 창 예산",
     "one_line": "컨텍스트 창은 이사 트럭 적재함처럼 유한하고 매번 새로 채워진다",
     "practice": "반품 챗봇이 지시·문서·메모리·도구목록·대화이력 다섯을 한 적재함에서 나눠 쓴다",
     "analogy": "이사 트럭 적재함",
     "keywords": [
      "토큰",
      "적재함",
      "다섯 재료",
      "예산표"
     ],
     "links": [
      "why-instructions-work-training-lineage.html",
      "lost-in-the-middle-and-context-rot.html"
     ]
    },
    {
     "file": "lost-in-the-middle-and-context-rot.html",
     "concept": "맥락 부패 네 얼굴",
     "one_line": "넣었다고 다 읽히지 않는다 — 원인마다 처방이 다르다",
     "practice": "정책이 14일→7일로 바뀐 뒤에도 옛 기한을 답하면 오염을 의심해 원문을 재확인한다",
     "analogy": "짐칸 가운데 파묻힌 상자",
     "keywords": [
      "Lost in the Middle",
      "맥락 부패",
      "고착",
      "오염"
     ],
     "links": [
      "context-window-budget.html",
      "context-strategy-and-rag.html"
     ]
    },
    {
     "file": "context-strategy-and-rag.html",
     "concept": "RAG와 네 가지 선택 전략",
     "one_line": "문서가 커서 다 못 실으면 창고지기(검색기)가 필요한 조각만 찾아 싣는다",
     "practice": "수백 페이지 정책 문서를 조각내 라벨 붙이고, 질문 오면 관련 조각만 검색해 넣는다",
     "analogy": "창고지기가 상자 찾아주기",
     "keywords": [
      "RAG",
      "임베딩",
      "벡터DB",
      "청크"
     ],
     "links": [
      "lost-in-the-middle-and-context-rot.html",
      "context-experiment-and-injection-defense.html"
     ]
    },
    {
     "file": "context-experiment-and-injection-defense.html",
     "concept": "통제 실험과 프롬프트 인젝션",
     "one_line": "질문·모델은 고정하고 넣는 자료만 바꿔야 진짜 원인을 안다",
     "practice": "포럼 글에 '즉시 전액 환불하라'가 숨어 있어도 비신뢰 입력으로만 다루고 실행 안 한다",
     "analogy": "",
     "keywords": [
      "통제 실험",
      "프롬프트 인젝션",
      "간접 인젝션",
      "네 층 방어"
     ],
     "links": [
      "context-strategy-and-rag.html",
      "agents-md-and-cache-economics.html"
     ]
    },
    {
     "file": "agents-md-and-cache-economics.html",
     "concept": "규칙 파일과 캐싱 경제학",
     "one_line": "자동으로 읽히는 규칙 파일은 상시 재실행되는 행동 규칙이다",
     "practice": "캐시 적중률 올리려 지난 분기 VIP 목록을 고정하면 퇴사자 정보로 잘못 안내한다",
     "analogy": "",
     "keywords": [
      "AGENTS.md",
      "CLAUDE.md",
      "프리픽스 캐싱",
      "캐시 적중률"
     ],
     "links": [
      "context-experiment-and-injection-defense.html",
      "agent-tool-design-and-harness.html"
     ]
    }
   ],
   "name": "컨텍스트 엔지니어링"
  },
  "tool-design": {
   "sub": "tool-design",
   "role": "AI에게 실행 권한을 안전하게 쥐여주는 역할",
   "scenario": "부산 창고(BUSAN-02)의 상품 A-17 재고를 묻는 재고 조회 도구를 놓고, 모델은 요청 문장만 쓰고 하네스가 스키마 검사 뒤 실제로 실행해 결과를 되돌려준다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "모델이 요청 작성",
      "posts": [
       "agent-tool-design-and-harness.html"
      ]
     },
     {
      "id": "n2",
      "label": "하네스가 검증",
      "posts": [
       "agent-tool-design-and-harness.html"
      ]
     },
     {
      "id": "n3",
      "label": "도구 정의서 작성",
      "posts": [
       "tool-contract-and-schema.html"
      ]
     },
     {
      "id": "n4",
      "label": "스키마로 입력 제한",
      "posts": [
       "tool-contract-and-schema.html"
      ]
     },
     {
      "id": "n5",
      "label": "서버가 실행·권한 검사",
      "posts": [
       "tool-permission-and-evaluation.html"
      ]
     },
     {
      "id": "n6",
      "label": "결과 기록·회귀 판정",
      "posts": [
       "tool-permission-and-evaluation.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "요청 전달"
     ],
     [
      "n2",
      "n3",
      "계약 필요"
     ],
     [
      "n3",
      "n4",
      "입력 규격화"
     ],
     [
      "n4",
      "n5",
      "실행 전 검사"
     ],
     [
      "n5",
      "n6",
      "결과 기록"
     ],
     [
      "n6",
      "n1",
      "재실행"
     ]
    ]
   },
   "posts": [
    {
     "file": "agent-tool-design-and-harness.html",
     "concept": "모델·도구·에이전트·하네스",
     "one_line": "모델은 요청 문장만 쓰고, 하네스가 검증해 실제로 실행한다",
     "practice": "부산 창고 A-17 재고를 물으면 모델은 요청만 쓰고 하네스가 실행한다",
     "analogy": "",
     "keywords": [
      "하네스",
      "MCP",
      "function calling",
      "루프"
     ],
     "links": [
      "agents-md-and-cache-economics.html",
      "tool-contract-and-schema.html"
     ]
    },
    {
     "file": "tool-contract-and-schema.html",
     "concept": "도구 정의서 여섯 칸",
     "one_line": "이름·하는일·입력·반환·실패처리 여섯 칸으로 도구를 계약한다",
     "practice": "설명 문장 하나만 바꿔 같은 요청을 두 번 돌려 결과가 달라지는지 본다",
     "analogy": "",
     "keywords": [
      "도구 정의서",
      "스키마",
      "enum",
      "트레이스"
     ],
     "links": [
      "agent-tool-design-and-harness.html",
      "tool-permission-and-evaluation.html",
      "codeact-code-as-agent-actions.html",
      "generative-ai-design-patterns-ch2.html"
     ]
    },
    {
     "file": "tool-permission-and-evaluation.html",
     "concept": "최소 권한과 회귀 판정",
     "one_line": "실제로 막는 건 설명 문장이 아니라 서버 쪽 검증이다",
     "practice": "수량 바꾸는 도구는 기본 권한에서 빼고 별도 승인·서버 검사를 거치게 한다",
     "analogy": "",
     "keywords": [
      "최소 권한",
      "프롬프트 인젝션",
      "회귀",
      "스코어카드"
     ],
     "links": [
      "tool-contract-and-schema.html",
      "context-experiment-and-injection-defense.html"
     ]
    }
   ],
   "name": "도구 설계"
  },
  "paper-notes": {
   "sub": "paper-notes",
   "role": "도구 호출 형식 자체를 설계 대상으로 보는 역할",
   "scenario": "파일 수십 개를 같은 방식으로 바꿔야 할 때, 도구를 한 번씩 JSON으로 부르는 대신 파이썬 반복문 한 줄로 묶어 코드 자체를 행동으로 실행시킨다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "관찰 받기",
      "posts": [
       "codeact-code-as-agent-actions.html"
      ]
     },
     {
      "id": "n2",
      "label": "코드로 행동 작성",
      "posts": [
       "codeact-code-as-agent-actions.html"
      ]
     },
     {
      "id": "n3",
      "label": "실행·에러 메시지 받기",
      "posts": [
       "codeact-code-as-agent-actions.html"
      ]
     },
     {
      "id": "n4",
      "label": "스스로 고쳐 재실행",
      "posts": [
       "codeact-code-as-agent-actions.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "행동 결정"
     ],
     [
      "n2",
      "n3",
      "코드 실행"
     ],
     [
      "n3",
      "n4",
      "에러 나면"
     ],
     [
      "n4",
      "n3",
      "다시 실행"
     ]
    ]
   },
   "posts": [
    {
     "file": "codeact-code-as-agent-actions.html",
     "concept": "CodeAct 코드 행동",
     "one_line": "도구를 하나씩 부르는 대신 코드로 행동을 적어 여러 호출을 묶는다",
     "practice": "파일 10개를 처리할 때 반복문 한 줄로 묶어 최대 30% 적은 행동 수로 끝낸다",
     "analogy": "",
     "keywords": [
      "CodeAct",
      "자기 디버깅",
      "M3ToolEval",
      "샌드박스"
     ],
     "links": [
      "tool-contract-and-schema.html",
      "agent-tool-design-and-harness.html"
     ]
    }
   ],
   "name": "논문"
  },
  "chatbot-project": {
   "sub": "chatbot-project",
   "role": "PRD부터 배포까지 근거 있는 RAG 챗봇을 직접 설계·구현한다",
   "scenario": "모두콘 안내 챗봇처럼 서버 비용 없이 GitHub Pages에 배포하고, 방문자의 브라우저와 로컬 Ollama만으로 질문에 근거 문서와 판정 배지를 함께 보여주는 서비스를 만들 때 쓰인다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "기획·설계",
      "posts": [
       "rag-chatbot-project-overview.html",
       "rag-chatbot-prd-questions.html"
      ]
     },
     {
      "id": "n2",
      "label": "자료·청크화",
      "posts": [
       "rag-chatbot-chunk-design.html"
      ]
     },
     {
      "id": "n3",
      "label": "임베딩·벡터화",
      "posts": [
       "rag-chatbot-embedding-vectorstore.html"
      ]
     },
     {
      "id": "n4",
      "label": "하이브리드검색",
      "posts": [
       "rag-chatbot-hybrid-search.html"
      ]
     },
     {
      "id": "n5",
      "label": "생성·스트리밍",
      "posts": [
       "rag-chatbot-prompt-streaming.html"
      ]
     },
     {
      "id": "n6",
      "label": "판정·실험",
      "posts": [
       "rag-chatbot-llm-judge.html",
       "rag-chatbot-prompt-experiment.html"
      ]
     },
     {
      "id": "n7",
      "label": "배포·제출",
      "posts": [
       "rag-chatbot-submission.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "자료를 모은다"
     ],
     [
      "n2",
      "n3",
      "벡터로 바꾼다"
     ],
     [
      "n3",
      "n4",
      "검색한다"
     ],
     [
      "n4",
      "n5",
      "근거로 답한다"
     ],
     [
      "n5",
      "n6",
      "심사한다"
     ],
     [
      "n6",
      "n7",
      "배포한다"
     ]
    ]
   },
   "posts": [
    {
     "file": "rag-chatbot-project-overview.html",
     "concept": "RAG 파이프라인 개관",
     "one_line": "질문이 판정 배지까지 가는 6단계 그림을 먼저 그린다",
     "practice": "회사 자료만 보고 답하는 챗봇을 기획할 때 6단계 설계 지도로 쓴다",
     "analogy": "근거를 짚고 확신도까지 보고하는 직원",
     "keywords": [
      "RAG",
      "GitHub Pages",
      "로컬 Ollama",
      "근거 청크",
      "판정 배지"
     ],
     "links": [
      "tool-permission-and-evaluation.html",
      "running-local-llm-with-ollama.html",
      "connecting-frontend-backend.html"
     ]
    },
    {
     "file": "rag-chatbot-prd-questions.html",
     "concept": "PRD 여덟 질문",
     "one_line": "코드 전에 성공 기준과 하지 않을 일을 여덟 질문으로 고정한다",
     "practice": "챗봇을 기획할 때 목표·비목표·수용기준을 먼저 문장으로 고정한다",
     "analogy": "",
     "keywords": [
      "PRD",
      "비목표",
      "수용 기준",
      "결정 필요",
      "바이브 코딩"
     ],
     "links": [
      "my-harness-users-and-prd.html"
     ]
    },
    {
     "file": "rag-chatbot-chunk-design.html",
     "concept": "청크 설계",
     "one_line": "검색되는 문장과 근거로 확인 가능한 문장은 다르다",
     "practice": "자료를 모을 때 본문에 원문 URL·섹션을 함께 저장해 출처를 남긴다",
     "analogy": "",
     "keywords": [
      "청크",
      "출처 URL",
      "사실 단위",
      "최소 120자",
      "검증 필요"
     ],
     "links": []
    },
    {
     "file": "rag-chatbot-embedding-vectorstore.html",
     "concept": "임베딩·벡터스토어",
     "one_line": "문장을 768차원 숫자로 바꿔 질문과 가까운 근거를 찾는 색인 과정",
     "practice": "문서와 질문을 임베딩할 때 같은 모델·풀링·정규화 경로를 맞춘다",
     "analogy": "",
     "keywords": [
      "임베딩",
      "벡터스토어",
      "mean pooling",
      "L2 정규화",
      "Cache Storage"
     ],
     "links": []
    },
    {
     "file": "rag-chatbot-hybrid-search.html",
     "concept": "하이브리드 검색",
     "one_line": "의미로 찾는 코사인과 낱말로 찾는 BM25를 합쳐 구멍을 메운다",
     "practice": "검색 결과가 미덥지 않을 때 임계값보다 먼저 임베딩 경로와 청크 경계를 점검한다",
     "analogy": "",
     "keywords": [
      "코사인 유사도",
      "BM25",
      "하이브리드 검색",
      "약한 근거 0.55",
      "중복 제거"
     ],
     "links": [
      "graphrag-why-multihop.html"
     ]
    },
    {
     "file": "rag-chatbot-prompt-streaming.html",
     "concept": "프롬프트 조립·스트리밍",
     "one_line": "근거 원칙을 프롬프트에 고정하고 로컬 LLM이 스트리밍으로 답한다",
     "practice": "배포한 챗봇이 답을 못 받아올 때 OLLAMA_ORIGINS 설정부터 확인한다",
     "analogy": "",
     "keywords": [
      "buildPrompt",
      "스트리밍",
      "AbortSignal",
      "OLLAMA_ORIGINS",
      "CORS"
     ],
     "links": [
      "connecting-frontend-backend.html",
      "running-local-llm-with-ollama.html"
     ]
    },
    {
     "file": "rag-chatbot-llm-judge.html",
     "concept": "LLM-as-a-Judge",
     "one_line": "답변 뒤에 별도 평가자를 두어 근거성·환각·인용·거부를 판정한다",
     "practice": "그럴듯하게 틀린 답이 걱정될 때 답변 뒤에 자동 심사위원을 하나 더 둔다",
     "analogy": "답변 뒤에 앉은 심사위원",
     "keywords": [
      "LLM-as-a-Judge",
      "grounded",
      "refusal",
      "환각",
      "judgeError"
     ],
     "links": [
      "graphrag-goldenset-eval.html",
      "multi-agent-judging-records.html",
      "langgraph-pattern-evaluator-optimizer.html"
     ]
    },
    {
     "file": "rag-chatbot-prompt-experiment.html",
     "concept": "루브릭 실험",
     "one_line": "고정 질문 세트로 한 번에 하나씩 바꿔가며 개선을 기록으로 증명한다",
     "practice": "설정을 바꿔 좋아진 것 같을 때 변수 하나만 바꾸고 판정 필드를 기록으로 남긴다",
     "analogy": "",
     "keywords": [
      "루브릭",
      "고정 질문 세트",
      "한 번에 하나",
      "README 기록",
      "grounded 비율"
     ],
     "links": []
    },
    {
     "file": "rag-chatbot-submission.html",
     "concept": "배포·제출",
     "one_line": "스키마·파이프라인은 그대로 두고 자료만 내 도메인으로 갈아끼운다",
     "practice": "예제 챗봇을 내 자료로 바꿀 때 스키마·파이프라인은 고정하고 자료만 교체한다",
     "analogy": "",
     "keywords": [
      "base 경로",
      "OLLAMA_ORIGINS",
      "README",
      "PRD.md",
      "사용 조건"
     ],
     "links": []
    }
   ],
   "name": "나만의 챗봇 만들기"
  },
  "mcp-skill-series": {
   "sub": "mcp-skill-series",
   "role": "MCP로 도구를 잇고 Skill로 팀 판단 기준을 굳히는 역할",
   "scenario": "가상 제품팀의 주간 업무 기록을 MCP 서버로 읽어와, 배포와 운영 확인까지 끝난 것만 완료로 보는 팀 규칙을 SKILL.md에 담아 매주 같은 기준으로 보고서를 쓰는 데 쓰인다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "도구 호출 이해",
      "posts": [
       "mcp-skill-tool-call-anatomy.html",
       "mcp-skill-protocol-roles.html"
      ]
     },
     {
      "id": "n2",
      "label": "MCP 서버 구축",
      "posts": [
       "mcp-skill-building-server.html",
       "mcp-skill-host-connection.html"
      ]
     },
     {
      "id": "n3",
      "label": "문맥 관리",
      "posts": [
       "mcp-skill-context-and-search.html"
      ]
     },
     {
      "id": "n4",
      "label": "Skill로 판정 고정",
      "posts": [
       "mcp-skill-why-skill-needed.html",
       "mcp-skill-first-weekly-report.html",
       "mcp-skill-writing-skill-md.html"
      ]
     },
     {
      "id": "n5",
      "label": "재사용 검증",
      "posts": [
       "mcp-skill-reuse-verification.html"
      ]
     },
     {
      "id": "n6",
      "label": "외부 연결 확장",
      "posts": [
       "mcp-skill-colab-notebook.html",
       "mcp-skill-google-oauth-setup.html",
       "mcp-skill-google-sheets-mcp.html"
      ]
     },
     {
      "id": "n7",
      "label": "내 업무 적용·지식화",
      "posts": [
       "mcp-skill-adapting-to-my-task.html",
       "mcp-skill-wikiskill-research.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "직접 만든다"
     ],
     [
      "n2",
      "n3",
      "붙이고 늘린다"
     ],
     [
      "n3",
      "n4",
      "기준을 정한다"
     ],
     [
      "n4",
      "n5",
      "다음 주 재본다"
     ],
     [
      "n5",
      "n6",
      "연결을 넓힌다"
     ],
     [
      "n6",
      "n7",
      "내 업무화한다"
     ]
    ]
   },
   "posts": [
    {
     "file": "mcp-skill-tool-call-anatomy.html",
     "concept": "도구 호출 3단계",
     "one_line": "모델은 주문표만 만들고 실행은 프로그램이 대신 한다",
     "practice": "AI에게 사내 조회 기능을 맡기기 전에 도구 이름·설명·입력 스키마부터 정한다",
     "analogy": "홀 직원이 주문표를 적고 주방이 요리한다",
     "keywords": [
      "도구 정의",
      "입력 스키마",
      "파싱",
      "tool_use",
      "vLLM 파서"
     ],
     "links": [
      "agent-tool-design-and-harness.html",
      "tool-contract-and-schema.html",
      "langgraph-branches-and-tool-loop.html"
     ]
    },
    {
     "file": "mcp-skill-protocol-roles.html",
     "concept": "MCP 연결 구조",
     "one_line": "호스트 안 클라이언트가 서버와 tools/list·tools/call로 대화한다",
     "practice": "같은 조회 기능을 여러 앱에 붙일 때 MCP 서버 하나만 만들어 공통 규칙으로 연결한다",
     "analogy": "회사 대표번호 교환대가 부서로 내선을 이어준다",
     "keywords": [
      "호스트",
      "클라이언트",
      "서버",
      "JSON-RPC",
      "stdio"
     ],
     "links": [
      "mcp-usb-c-for-ai.html",
      "ai-skills-and-rules-files.html"
     ]
    },
    {
     "file": "mcp-skill-building-server.html",
     "concept": "Python MCP 서버",
     "one_line": "함수에 @mcp.tool() 한 줄을 붙이면 AI가 부를 수 있는 도구가 된다",
     "practice": "회사 파일을 AI가 못 읽을 때 파이썬 함수를 도구로 등록하고 경로를 코드 기준으로 고정한다",
     "analogy": "안내판에 이름 올린 신입 직원",
     "keywords": [
      "@mcp.tool()",
      "docstring",
      "uv",
      "가상환경",
      "WEEK_FILES"
     ],
     "links": []
    },
    {
     "file": "mcp-skill-host-connection.html",
     "concept": "서버 등록·연결 확인",
     "one_line": "설정에 이름·명령·절대경로를 적어야 호스트가 서버를 찾아 띄운다",
     "practice": "MCP 서버를 만들고도 안 될 때 연결→호출→원본 대조 세 단계로 나눠 확인한다",
     "analogy": "전화번호부에 올려야 교환대가 연결한다",
     "keywords": [
      "--directory",
      "절대 경로",
      "uv run --locked",
      "호출 기록",
      "PATH"
     ],
     "links": []
    },
    {
     "file": "mcp-skill-context-and-search.html",
     "concept": "문맥 부담 줄이기",
     "one_line": "도구 설명을 다 읽으면 실행 전, 결과가 크면 실행 후 부담이 생긴다",
     "practice": "연결한 도구가 늘어 AI가 느려질 때 실행 전·후 부담을 나눠 원인을 진단한다",
     "analogy": "회의 전 책상에 매뉴얼 100권 대신 색인 카드만 두기",
     "keywords": [
      "Tool Search",
      "지연 로딩",
      "Code Mode",
      "네임스페이스",
      "문맥 창"
     ],
     "links": [
      "context-window-budget.html",
      "lost-in-the-middle-and-context-rot.html"
     ]
    },
    {
     "file": "mcp-skill-why-skill-needed.html",
     "concept": "Skill의 필요성",
     "one_line": "같은 기록도 '개발 완료'만 보면 팀마다 다르게 판정한다",
     "practice": "AI가 자료는 잘 가져오는데 팀 기준과 다르게 판정할 때 그 기준을 Skill로 적어 둔다",
     "analogy": "도장 세 칸 중 어디까지가 끝인지는 방침이 정한다",
     "keywords": [
      "업무 고유 지식",
      "SKILL.md",
      "점진 공개",
      "3P",
      "brand-guidelines"
     ],
     "links": [
      "ai-skills-and-rules-files.html"
     ]
    },
    {
     "file": "mcp-skill-first-weekly-report.html",
     "concept": "규칙 대입 판정",
     "one_line": "위험→완료→진행 순서로 업무 하나를 한 범주에만 넣는다",
     "practice": "보고서를 쓸 때 기한은 컴퓨터 오늘 날짜가 아니라 기록 속 보고 기준일과 비교한다",
     "analogy": "병원 접수창구가 위험 신호부터 훑고 완료를 확인한다",
     "keywords": [
      "위험→완료→진행",
      "report_date",
      "null",
      "사실·판단·제안",
      "근거 필드"
     ],
     "links": []
    },
    {
     "file": "mcp-skill-writing-skill-md.html",
     "concept": "SKILL.md 작성",
     "one_line": "다음 주에도 맞는 문장만 골라 파일 하나로 옮기는 게 Skill 만들기다",
     "practice": "이번 주 정답과 다음에도 쓸 규칙을 가를 때 '다음 입력에도 맞나' 한 질문으로 판별한다",
     "analogy": "오늘 접시 대신 다음에도 통할 레시피를 붙인다",
     "keywords": [
      "frontmatter",
      "name·description",
      "references",
      "상대경로",
      "skills 폴더"
     ],
     "links": []
    },
    {
     "file": "mcp-skill-reuse-verification.html",
     "concept": "Skill 재사용 검증",
     "one_line": "새 대화·이름 없이 불러도 같은 기준이 적용돼야 진짜 검증이다",
     "practice": "Skill을 만든 뒤에는 반드시 새 대화를 열어 이름을 대지 않고 재사용되는지 확인한다",
     "analogy": "대타가 메모만으로 일했을 때 메모의 실력을 안다",
     "keywords": [
      "새 대화 검증",
      "near-miss",
      "기준선",
      "네 축 확인",
      "재현"
     ],
     "links": []
    },
    {
     "file": "mcp-skill-colab-notebook.html",
     "concept": "Colab 계산 기록",
     "one_line": "노트북 셀에 코드를 적는 것과 실제로 실행하는 것은 다른 일이다",
     "practice": "계산 근거를 남기고 싶을 때 입력·코드·결과·기준을 한 노트북에 나란히 적는다",
     "analogy": "레시피 공책에 적는 일과 실제 조리하는 일은 다르다",
     "keywords": [
      "셀",
      "런타임",
      "add_code_cell",
      "run_code_cell",
      "Cannot save changes"
     ],
     "links": []
    },
    {
     "file": "mcp-skill-google-oauth-setup.html",
     "concept": "Google OAuth 준비",
     "one_line": "로그인해 있어도 프로그램은 내 표를 읽을 동의를 따로 받아야 한다",
     "practice": "구글 시트를 읽는 프로그램을 만들 때 범위는 읽기 전용으로 좁히고 인증 파일은 커밋하지 않는다",
     "analogy": "사원증 있어도 외부 기사는 방문증을 따로 받는다",
     "keywords": [
      "OAuth",
      "scope",
      "credentials.json",
      "token.json",
      "Test users"
     ],
     "links": [
      "ai-code-security-basics.html"
     ]
    },
    {
     "file": "mcp-skill-google-sheets-mcp.html",
     "concept": "인증 코드와 시트 읽기",
     "one_line": "token.json이 한 번의 허용을 저장해 그다음부터 사람 없이 표를 읽는다",
     "practice": "구글 표를 도구로 공개할 때 시트 이름을 먼저 물어 범위 문자열을 조립한 뒤 값을 읽는다",
     "analogy": "방문증 넣어두면 데스크를 다시 안 부른다",
     "keywords": [
      "localhost",
      "포트",
      "load_token",
      "read_sheet_header",
      "ToolError"
     ],
     "links": []
    },
    {
     "file": "mcp-skill-adapting-to-my-task.html",
     "concept": "데이터·기준·기능 분리",
     "one_line": "자료를 바꾸면 그 의미와 좋은 결과의 기준도 함께 바꿔야 한다",
     "practice": "예제 실습을 내 업무로 옮길 때 데이터·업무 지식·실행 기능을 각각 따로 판단해 바꾼다",
     "analogy": "메뉴 바뀌면 재료·레시피는 바뀌어도 냄비는 그대로다",
     "keywords": [
      "데이터",
      "업무 지식",
      "실행 기능",
      "다섯 줄 설계표",
      "README"
     ],
     "links": []
    },
    {
     "file": "mcp-skill-wikiskill-research.html",
     "concept": "경험·지식·절차 분리",
     "one_line": "실행 경험을 지식으로 추린 뒤에야 절차(Skill)를 고쳐야 한다",
     "practice": "지침을 고친 뒤에는 반드시 예전 입력으로 다시 재서 나빠지면 되돌린다",
     "analogy": "정비소 일지·사례집·점검카드는 서로 다른 종이다",
     "keywords": [
      "WikiSkill",
      "실행 경험",
      "영속 지식",
      "검증 관문",
      "벤치마크"
     ],
     "links": []
    }
   ],
   "name": "MCP와 Skill로 업무 맡기기"
  },
  "langgraph-basics": {
   "sub": "langgraph-basics",
   "role": "LangGraph로 에이전트 워크플로의 뼈대를 설계하는 기초 단계",
   "scenario": "뉴스레터·CS 상담 에이전트를 만들기 전, 간 맞추기·노트 분량 검사 같은 작은 그래프로 State·Node·Edge와 조건부 엣지, 도구 루프를 손으로 조립해 보며 이후 실전 프로젝트의 뼈대를 다졌다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "워크플로vs에이전트 판단",
      "posts": [
       "langgraph-what-and-why.html"
      ]
     },
     {
      "id": "n2",
      "label": "State·Node·Edge 설계",
      "posts": [
       "langgraph-state-node-edge.html"
      ]
     },
     {
      "id": "n3",
      "label": "조건부 엣지로 분기",
      "posts": [
       "langgraph-branch-drills.html"
      ]
     },
     {
      "id": "n4",
      "label": "도구 루프로 자율성",
      "posts": [
       "langgraph-branches-and-tool-loop.html"
      ]
     },
     {
      "id": "n5",
      "label": "API 키 환경 설정",
      "posts": [
       "langgraph-env-troubleshooting.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "구조를 짠다"
     ],
     [
      "n2",
      "n3",
      "갈래를 늘림"
     ],
     [
      "n3",
      "n4",
      "판단을 위임"
     ],
     [
      "n4",
      "n5",
      "실행 준비"
     ]
    ]
   },
   "posts": [
    {
     "file": "langgraph-what-and-why.html",
     "concept": "워크플로 vs 에이전트",
     "one_line": "다음 함수를 누가 고르는지가 워크플로와 에이전트를 가른다",
     "practice": "자동화를 설계할 때 순서를 사람이 못 박을지 AI가 매번 고르게 할지부터 정한다",
     "analogy": "동선표 있는 A주방 vs 주방장 즉흥 판단하는 B주방",
     "keywords": [
      "워크플로",
      "에이전트",
      "조건부 엣지",
      "자율성 눈금자"
     ],
     "links": [
      "what-is-automation-workflow-agent.html",
      "n8n-agent-delegation-and-if-node.html",
      "multi-agent-three-runs-abc.html",
      "what-is-ai-agent.html"
     ]
    },
    {
     "file": "langgraph-state-node-edge.html",
     "concept": "State·Node·Edge",
     "one_line": "State는 전표, Node는 일하는 함수, Edge는 다음 길을 정하는 선이다",
     "practice": "여러 단계 파이프라인을 짤 때 노드가 바뀐 칸만 돌려주게 설계한다",
     "analogy": "전표가 도는 주방, 조리대마다 칸만 체크",
     "keywords": [
      "State",
      "부분 업데이트",
      "TypedDict",
      "트레이스백"
     ],
     "links": [
      "langgraph-what-and-why.html",
      "reading-python-code-basics.html",
      "n8n-agent-delegation-and-if-node.html",
      "my-harness-flow-and-state.html"
     ]
    },
    {
     "file": "langgraph-branch-drills.html",
     "concept": "갈림길·라벨·반복",
     "one_line": "갈래를 늘릴 땐 목적지 목록도 함께 고쳐야 새는 입력이 없다",
     "practice": "고객 문의 갈래가 하나 늘 때 라우터와 목적지 목록을 같이 고치고 무한반복을 막는다",
     "analogy": "검수대에 소분대가 새로 생긴 주방",
     "keywords": [
      "조건부 엣지",
      "라벨",
      "recursion_limit",
      "라우터"
     ],
     "links": [
      "langgraph-state-node-edge.html",
      "n8n-agent-delegation-and-if-node.html",
      "my-harness-flow-and-state.html"
     ]
    },
    {
     "file": "langgraph-branches-and-tool-loop.html",
     "concept": "도구 호출 루프",
     "one_line": "모델은 도구 요청서만 쓰고 실행은 ToolNode가 대신 한다",
     "practice": "날짜 계산처럼 틀리면 곤란한 계산은 LLM 대신 도구 함수로 떼어 정확도를 지킨다",
     "analogy": "홀 직원의 창고 조회 요청서",
     "keywords": [
      "ToolNode",
      "bind_tools",
      "ReAct",
      "독스트링"
     ],
     "links": [
      "agent-react-loop-and-autogpt.html",
      "mcp-skill-tool-call-anatomy.html",
      "langgraph-what-and-why.html",
      "cs-agent-grounding.html"
     ]
    },
    {
     "file": "langgraph-env-troubleshooting.html",
     "concept": "원격 주피터 API 키",
     "one_line": ".env가 안 읽히면 대개 실행 위치·설치·override 순서 문제다",
     "practice": "Colab에서 API 키를 못 읽을 때 작업 폴더부터 확인하고 원인을 순서대로 걷어낸다",
     "analogy": "남의 식당 주방을 빌려 하루 장사하기",
     "keywords": [
      ".env",
      "python-dotenv",
      "환경 변수",
      "override"
     ],
     "links": [
      "ai-code-security-basics.html",
      "mcp-skill-google-sheets-mcp.html",
      "why-gpu-and-colab-cli.html",
      "langgraph-branches-and-tool-loop.html"
     ]
    }
   ],
   "name": "LangGraph 기초 — State·Node·Edge"
  },
  "langgraph-patterns": {
   "sub": "langgraph-patterns",
   "role": "다섯 가지 워크플로 패턴으로 LLM 파이프라인 짜기",
   "scenario": "체이닝·라우팅·병렬화·오케스트레이터-워커·평가자-최적화자 다섯 모양을 학습 노트 검사·문의 분류 같은 예제로 실습한 뒤, 이후 뉴스레터·CS·GraphRAG 에이전트에서 그대로 재사용했다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "단계 순서 고정",
      "posts": [
       "langgraph-pattern-chaining.html"
      ]
     },
     {
      "id": "n2",
      "label": "입력별 갈래 분기",
      "posts": [
       "langgraph-pattern-routing.html"
      ]
     },
     {
      "id": "n3",
      "label": "동시 처리+개수 고정",
      "posts": [
       "langgraph-pattern-parallelization.html"
      ]
     },
     {
      "id": "n4",
      "label": "개수 실행중 결정",
      "posts": [
       "langgraph-pattern-orchestrator-worker.html"
      ]
     },
     {
      "id": "n5",
      "label": "기준 통과까지 반복",
      "posts": [
       "langgraph-pattern-evaluator-optimizer.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "종류별 분기"
     ],
     [
      "n2",
      "n3",
      "동시 가능하면"
     ],
     [
      "n3",
      "n4",
      "개수 모르면"
     ],
     [
      "n4",
      "n5",
      "반복 개선하면"
     ]
    ]
   },
   "posts": [
    {
     "file": "langgraph-pattern-chaining.html",
     "concept": "프롬프트 체이닝",
     "one_line": "순서 고정 단계 사이에 코드 게이트를 끼워 틀린 중간 결과를 막는다",
     "practice": "초안 작성 후 용어 누락을 코드로 검사하고 통과해야 다음 단계로 넘긴다",
     "analogy": "코스 요리와 단계 사이 검수대",
     "keywords": [
      "게이트",
      "결정적 검사",
      "LLM 게이트",
      "단계 분리"
     ],
     "links": [
      "langgraph-what-and-why.html",
      "output-format-and-metrics.html",
      "langgraph-pattern-routing.html"
     ]
    },
    {
     "file": "langgraph-pattern-routing.html",
     "concept": "라우팅",
     "one_line": "LLM이 입력을 분류해 미리 그은 갈래 중 하나로만 보낸다",
     "practice": "고객 문의를 종류별로 나눠 각각 다른 프롬프트로 처리할 때 이 모양을 쓴다",
     "analogy": "주문서를 읽는 매니저",
     "keywords": [
      "구조화 출력",
      "Literal",
      "분류",
      "확신도"
     ],
     "links": [
      "langgraph-pattern-chaining.html",
      "cs-agent-routing-eval.html",
      "output-format-and-metrics.html"
     ]
    },
    {
     "file": "langgraph-pattern-parallelization.html",
     "concept": "병렬화",
     "one_line": "독립적인 일을 동시에 돌리고 리듀서로 결과를 합친다",
     "practice": "한 초안을 여러 평가 기준으로 동시에 채점할 때 리듀서로 결과를 모은다",
     "analogy": "검사 담당 셋이 한 접시를 동시에",
     "keywords": [
      "리듀서",
      "operator.add",
      "슈퍼스텝",
      "InvalidUpdateError"
     ],
     "links": [
      "langgraph-pattern-routing.html",
      "langgraph-pattern-orchestrator-worker.html",
      "newsletter-agent-select.html"
     ]
    },
    {
     "file": "langgraph-pattern-orchestrator-worker.html",
     "concept": "오케스트레이터-워커",
     "one_line": "LLM이 실행 중 워커 개수를 정해 Send로 동적으로 불러낸다",
     "practice": "회의록에서 나온 할 일 개수만큼 담당자 배정 초안을 만들 때 쓴다",
     "analogy": "헤드셰프가 그날 메뉴 수를 정한다",
     "keywords": [
      "Send",
      "맵-리듀스",
      "쪽지",
      "단일 실패 지점"
     ],
     "links": [
      "langgraph-pattern-parallelization.html",
      "langgraph-pattern-evaluator-optimizer.html",
      "newsletter-agent-summarize-verify.html"
     ]
    },
    {
     "file": "langgraph-pattern-evaluator-optimizer.html",
     "concept": "평가자-최적화자",
     "one_line": "생성과 평가를 오가며 기준을 넘을 때까지 되돌아가 고쳐 쓴다",
     "practice": "초안을 채점해 기준 미달이면 피드백을 실어 되돌리고 상한에서 정상 출구로 뺀다",
     "analogy": "시식 담당이 조리사에게 되돌린다",
     "keywords": [
      "정상 출구",
      "recursion_limit",
      "피드백",
      "롤백"
     ],
     "links": [
      "langgraph-pattern-orchestrator-worker.html",
      "cs-agent-improve.html",
      "langgraph-what-and-why.html"
     ]
    }
   ],
   "name": "에이전트 워크플로 다섯 패턴"
  },
  "newsletter-agent-project": {
   "sub": "newsletter-agent-project",
   "role": "매일 아침 뉴스를 골라 요약해 보내는 에이전트",
   "scenario": "AI 뉴스 100여 건 중 다섯 건을 골라 요약하고 원문과 대조해 디스코드로 매일 아침 발행하는 뉴스레터 에이전트를 처음부터 끝까지 만들고, 운영 뒤 실행 기록으로 매체별 성적을 다시 재는 과정까지 다뤘다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "뼈대 세우기",
      "posts": [
       "newsletter-agent-skeleton.html"
      ]
     },
     {
      "id": "n2",
      "label": "수집",
      "posts": [
       "newsletter-agent-collect.html"
      ]
     },
     {
      "id": "n3",
      "label": "선별",
      "posts": [
       "newsletter-agent-select.html"
      ]
     },
     {
      "id": "n4",
      "label": "요약·검수",
      "posts": [
       "newsletter-agent-summarize-verify.html"
      ]
     },
     {
      "id": "n5",
      "label": "발행·예약",
      "posts": [
       "newsletter-agent-publish-schedule.html"
      ]
     },
     {
      "id": "n6",
      "label": "실행 기록·설정",
      "posts": [
       "newsletter-agent-metrics-config.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "노드를 채움"
     ],
     [
      "n2",
      "n3",
      "후보 넘김"
     ],
     [
      "n3",
      "n4",
      "고른 기사 취재"
     ],
     [
      "n4",
      "n5",
      "통과분 발행"
     ],
     [
      "n5",
      "n6",
      "돌고 나서 잼"
     ]
    ]
   },
   "posts": [
    {
     "file": "newsletter-agent-skeleton.html",
     "concept": "걸어 다니는 뼈대",
     "one_line": "다섯 단계를 빈 함수로 먼저 이어 끝까지 도는 상태부터 만든다",
     "practice": "새 자동화 파이프라인을 짤 때 State 규격부터 고정하고 노드를 하나씩 진짜로 바꾼다",
     "analogy": "개업 전 리허설, 빈 접시로 한 바퀴",
     "keywords": [
      "walking skeleton",
      "리듀서",
      "State 설계",
      "draw_mermaid"
     ],
     "links": [
      "langgraph-pattern-evaluator-optimizer.html",
      "newsletter-agent-collect.html",
      "langgraph-what-and-why.html"
     ]
    },
    {
     "file": "newsletter-agent-collect.html",
     "concept": "수집 경로와 관문",
     "one_line": "발행자가 허락한 통로부터 쓰고 본문·생존·접근 관문 통과 소스만 채택한다",
     "practice": "새 RSS 소스를 추가하기 전 본문이 실제로 뽑히는지, 최근에도 글이 올라오는지 확인한다",
     "analogy": "새벽 장보기",
     "keywords": [
      "RSS",
      "trafilatura",
      "조용한 실패",
      "1차 소스"
     ],
     "links": [
      "newsletter-agent-skeleton.html",
      "newsletter-agent-select.html",
      "newsletter-agent-metrics-config.html"
     ]
    },
    {
     "file": "newsletter-agent-select.html",
     "concept": "예선·본선 선별",
     "one_line": "점수가 아니라 비교로, 묶음 예선을 거쳐 본선에서 다섯 건을 고른다",
     "practice": "후보 100여 건에서 정해진 개수만 고를 때 점수 매기기 대신 순서를 묻는다",
     "analogy": "재료를 한 도마에 올려 비교한다",
     "keywords": [
      "상대평가",
      "구조화 출력",
      "묶음 예선",
      "사건 라벨"
     ],
     "links": [
      "newsletter-agent-collect.html",
      "newsletter-agent-summarize-verify.html",
      "langgraph-pattern-parallelization.html"
     ]
    },
    {
     "file": "newsletter-agent-summarize-verify.html",
     "concept": "요약 세 칸·검수",
     "one_line": "대조 가능한 칸으로 요약을 나눠 받고 원문과 대조해 통과분만 남긴다",
     "practice": "AI가 쓴 글을 매번 사람이 안 읽고 내보낼 때 생성과 분리된 검수 호출을 둔다",
     "analogy": "칸 나눈 도시락과 그 시식 담당",
     "keywords": [
      "headline·summary·why",
      "팬아웃 경계",
      "환각",
      "LLM 대조"
     ],
     "links": [
      "newsletter-agent-select.html",
      "newsletter-agent-publish-schedule.html",
      "langgraph-pattern-orchestrator-worker.html"
     ]
    },
    {
     "file": "newsletter-agent-publish-schedule.html",
     "concept": "발행·예약 실행",
     "one_line": "검수 통과분을 디스코드로 보내고 GitHub Actions로 매일 자동 실행한다",
     "practice": "0건인 날도 조용함을 알리고, 실패 응답은 조용히 넘기지 않고 예외로 던진다",
     "analogy": "완성된 한 상을 손님 앞에 내보낸다",
     "keywords": [
      "웹훅",
      "dry-run",
      "GitHub Actions",
      "Secrets"
     ],
     "links": [
      "newsletter-agent-summarize-verify.html",
      "newsletter-agent-metrics-config.html"
     ]
    },
    {
     "file": "newsletter-agent-metrics-config.html",
     "concept": "실행 기록·설정 파일",
     "one_line": "실행마다 깔때기 건수를 한 줄로 남기고 편집 기준은 설정 파일로 뗀다",
     "practice": "며칠째 발행 기여가 0인 매체를 실행 기록만으로 찾아 뺄 근거를 만든다",
     "analogy": "장부와 레시피 카드",
     "keywords": [
      "JSONL",
      "깔때기 관측",
      "audience.yaml",
      "소스별 성적표"
     ],
     "links": [
      "newsletter-agent-publish-schedule.html",
      "newsletter-agent-collect.html"
     ]
    }
   ],
   "name": "뉴스레터 에이전트 만들기"
  },
  "cs-agent-project": {
   "sub": "cs-agent-project",
   "role": "회사 규정 근거로 조회해 답하는 CS 상담 에이전트",
   "scenario": "쇼핑몰 고객 문의를 다섯 갈래로 분류하고, 매뉴얼을 조회 도구로 연결해 근거 없는 숫자를 걸러낸 뒤, 실패 사례를 하나씩 뜯어 프롬프트를 고쳐 정확도를 59%에서 94%로 올렸다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "문의 분류 라우터",
      "posts": [
       "cs-agent-routing-eval.html"
      ]
     },
     {
      "id": "n2",
      "label": "규정 골라넣기",
      "posts": [
       "cs-agent-grounding.html"
      ]
     },
     {
      "id": "n3",
      "label": "도구 조회 루프",
      "posts": [
       "cs-agent-grounding.html"
      ]
     },
     {
      "id": "n4",
      "label": "가드레일 검사",
      "posts": [
       "cs-agent-grounding.html"
      ]
     },
     {
      "id": "n5",
      "label": "실패 분석·개선",
      "posts": [
       "cs-agent-improve.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "라우트별 매뉴얼"
     ],
     [
      "n2",
      "n3",
      "값 조회"
     ],
     [
      "n3",
      "n4",
      "답변 검사"
     ],
     [
      "n4",
      "n5",
      "실패 유형 분석"
     ]
    ]
   },
   "posts": [
    {
     "file": "cs-agent-routing-eval.html",
     "concept": "문의 분류 라우터",
     "one_line": "회사 매뉴얼에서 갈래와 기준을 가져와 문의를 다섯 갈래로 분류한다",
     "practice": "처리 종류가 하나 늘 때 감으로 갈래를 짓지 않고 업무 매뉴얼에서 갈래를 가져온다",
     "analogy": "주문서를 읽고, 애매하면 셰프를 부른다",
     "keywords": [
      "OTHER",
      "macro F1",
      "혼동 행렬",
      "확신도 이관"
     ],
     "links": [
      "langgraph-pattern-routing.html",
      "cs-agent-grounding.html",
      "cs-agent-improve.html"
     ]
    },
    {
     "file": "cs-agent-grounding.html",
     "concept": "그라운딩 세 겹",
     "one_line": "값을 외워 답하지 않고 조회하게 하고 숫자 출처를 기계로 검사한다",
     "practice": "규정이 자주 바뀌는 값을 챗봇이 안내할 때 상수 대신 조회 도구로 만든다",
     "analogy": "레시피 카드와 냉장고, 그리고 검수대",
     "keywords": [
      "그라운딩",
      "가드레일",
      "null 미확정",
      "도구 루프"
     ],
     "links": [
      "cs-agent-routing-eval.html",
      "cs-agent-improve.html",
      "langgraph-branches-and-tool-loop.html"
     ]
    },
    {
     "file": "cs-agent-improve.html",
     "concept": "실패 분석 기반 개선",
     "one_line": "실패 건을 유형별로 세고 한 번에 하나만 고쳐 두 번씩 재서 검증한다",
     "practice": "프롬프트를 고쳐 점수를 올릴 때 스냅샷을 남기고 반복 측정으로 운과 개선을 가른다",
     "analogy": "레시피 한 줄만 바꾸고 30접시를 다시 낸다",
     "keywords": [
      "기준선",
      "롤백",
      "스냅샷",
      "엔티티 링킹"
     ],
     "links": [
      "cs-agent-grounding.html",
      "cs-agent-routing-eval.html",
      "langgraph-pattern-evaluator-optimizer.html"
     ]
    }
   ],
   "name": "CS 상담 에이전트 만들기"
  },
  "graphrag-project": {
   "sub": "graphrag-project",
   "role": "멀티홉 질문에 답하려고 지식 그래프를 얹은 추천 에이전트",
   "scenario": "《기생충》 배우의 다른 작품처럼 문서 하나로 안 되는 멀티홉 질문에, 위키 문서에서 삼중항을 뽑아 그래프로 잇고 세 갈래 라우터로 답하게 한 뒤 BM25 검색과 같은 15문항으로 채점해 비교했다.",
   "flow": {
    "nodes": [
     {
      "id": "n1",
      "label": "검색 한계 측정",
      "posts": [
       "graphrag-why-multihop.html"
      ]
     },
     {
      "id": "n2",
      "label": "삼중항 추출·정규화",
      "posts": [
       "graphrag-build-knowledge-graph.html"
      ]
     },
     {
      "id": "n3",
      "label": "커뮤니티 요약",
      "posts": [
       "graphrag-agent-three-routes.html"
      ]
     },
     {
      "id": "n4",
      "label": "세 갈래 라우팅 답변",
      "posts": [
       "graphrag-agent-three-routes.html"
      ]
     },
     {
      "id": "n5",
      "label": "골든셋 채점",
      "posts": [
       "graphrag-goldenset-eval.html"
      ]
     }
    ],
    "edges": [
     [
      "n1",
      "n2",
      "그래프로 보강"
     ],
     [
      "n2",
      "n3",
      "무리 요약 준비"
     ],
     [
      "n3",
      "n4",
      "질문별 근거 수집"
     ],
     [
      "n4",
      "n5",
      "층별 채점"
     ]
    ]
   },
   "posts": [
    {
     "file": "graphrag-why-multihop.html",
     "concept": "멀티홉과 지식 그래프",
     "one_line": "검색은 문서 하나짜리 답만 찾고 여러 사실을 이어야 하는 질문은 못 찾는다",
     "practice": "챗봇이 A에 나온 사람의 다른 작품을 묻는 연결 질문에서 막힐 때 그래프 구조를 검토한다",
     "analogy": "레시피 카드 서랍과 벽에 붙인 연결판",
     "keywords": [
      "삼중항",
      "DiGraph",
      "Recall@K",
      "리랭킹 한계"
     ],
     "links": [
      "langgraph-pattern-routing.html",
      "graphrag-build-knowledge-graph.html",
      "confusion-matrix-and-metrics.html"
     ]
    },
    {
     "file": "graphrag-build-knowledge-graph.html",
     "concept": "삼중항 추출·정규화",
     "one_line": "답할 질문에서 거꾸로 스키마를 정하고 표기 다른 같은 대상을 한 점으로 합친다",
     "practice": "LLM으로 관계를 대량 추출하기 전 문서 몇 건으로 시험하고 토큰 비용부터 어림한다",
     "analogy": "직원에게 카드를 읽혀 연결판을 만든다",
     "keywords": [
      "LLMGraphTransformer",
      "strict_mode",
      "정규화",
      "위키 분류 규칙"
     ],
     "links": [
      "graphrag-why-multihop.html",
      "graphrag-agent-three-routes.html"
     ]
    },
    {
     "file": "graphrag-agent-three-routes.html",
     "concept": "세 갈래 그래프 라우팅",
     "one_line": "질문을 지역·경로·전역으로 나눠 각각 다른 근거로 답한다",
     "practice": "추천 기능에 왜 추천하는지 근거를 붙일 때 지나온 경로를 이유로 남긴다",
     "analogy": "홀 매니저가 질문을 세 갈래로 보낸다",
     "keywords": [
      "커뮤니티 탐지",
      "요구 관계",
      "탐색 예산",
      "흔한 매개 감점"
     ],
     "links": [
      "graphrag-build-knowledge-graph.html",
      "graphrag-goldenset-eval.html",
      "langgraph-pattern-orchestrator-worker.html"
     ]
    },
    {
     "file": "graphrag-goldenset-eval.html",
     "concept": "세 층 평가",
     "one_line": "색인·검색·생성 층을 나눠 재야 어디를 고칠지 안다",
     "practice": "새 검색 기법을 도입하기 전 같은 골든셋으로 지금 방식과 나란히 채점한다",
     "analogy": "시식 심사는 요리한 사람이 하지 않는다",
     "keywords": [
      "컨텍스트 재현율",
      "LLM 심판",
      "격자 탐색",
      "기준선 파일"
     ],
     "links": [
      "graphrag-agent-three-routes.html",
      "cs-agent-improve.html",
      "graphrag-why-multihop.html"
     ]
    }
   ],
   "name": "GraphRAG로 지식 그래프 얹기"
  }
 },
 "titles": {
  "learning-git-1.html": "Git 초보자 가이드 (1)",
  "learning-git-2.html": "GitHub 계정과 SSH 연결 (2)",
  "learning-git-3.html": "GitHub 클론·커밋·푸시 사용법 (3)",
  "learning-git-4.html": "GitHub Pages 무료 홈페이지 (4)",
  "learning-git-5.html": "GitHub Actions 예약 발행 (5)",
  "learning-git-6.html": "Git 브랜치·병합 실습 (6)",
  "git-commit-concept.html": "Git 커밋(commit)이란 무엇인가",
  "ssh-concept.html": "SSH 공개키·개인키 원리",
  "blog-seo-basics.html": "블로그 검색 노출(SEO) 기초",
  "what-is-vibe-coding.html": "바이브 코딩(Vibe Coding)이란?",
  "what-is-ai-token.html": "AI 토큰(Token)이란 무엇인가",
  "what-is-browser-cache.html": "브라우저 캐시(Cache)란 무엇인가",
  "what-is-github-contribution-graph.html": "GitHub 잔디심기란 무엇인가",
  "ai-agent-dev-environment.html": "Claude Code 개발 환경 세팅 (1)",
  "ai-agent-dev-environment-check.html": "Node.js·npm 설치 확인 (2)",
  "my-first-web-project.html": "Claude Code로 첫 웹페이지 만들기 (3)",
  "vibe-coding-loop.html": "AI 코딩 프롬프트 작성법 (4)",
  "terminal-shell-kernel-prompt.html": "터미널·셸·커널·프롬프트 차이 (5)",
  "terminal-practice.html": "PowerShell 명령어 실습 (6)",
  "ai-folder-cleanup.html": "Claude Code 파일 정리 자동화 (7)",
  "terminal-vs-ai-retrospective.html": "명령어 vs AI 자동화 비교 (8)",
  "translation-review-automation-idea.html": "AI 자막 감수 자동화 아이디어",
  "webpage-three-layers.html": "HTML·CSS·JS 3계층 구조 (1)",
  "javascript-event-loop-async.html": "CPU·코어·프로세스·스레드란? (2)",
  "ai-game-making-tetris-to-mine.html": "AI로 게임 만들기 — 테트리스에서 내 게임까지 (3)",
  "what-is-routing.html": "라우팅(Routing)이란 무엇인가",
  "what-is-api.html": "API란 무엇인가, AI와 차이",
  "what-is-framework.html": "프레임워크란 무엇인가",
  "what-is-abstraction-modularity.html": "추상화·모듈화·가상 DOM",
  "choosing-a-framework.html": "프레임워크 고르는 법과 AI와 기획하기",
  "mock-data-and-rest-api.html": "목업 데이터와 REST API",
  "why-backend-needed.html": "왜 화면 뒤에 서버가 필요할까",
  "domain-http-and-packets.html": "도메인·포트·HTTPS — 주소가 화면이 되기까지",
  "what-backend-actually-does.html": "백엔드가 실제로 하는 일",
  "ai-code-security-basics.html": "AI가 짠 백엔드 코드에서 반드시 확인할 것들",
  "deploying-and-free-hosting.html": "배포, 무료 호스팅, 집 컴퓨터를 서버로",
  "connecting-frontend-backend.html": "AI로 프론트-백엔드 연결하기",
  "what-is-proxy-server.html": "프록시 서버란 무엇인가 — API 키를 대신 들어주는 서버",
  "what-is-cors.html": "CORS란 무엇인가 — 다른 주소끼리 대화할 때 브라우저가 하는 검문",
  "what-is-docker.html": "도커(Docker)란 무엇인가 — 이미지와 컨테이너, 상자에 뭘 담느냐",
  "why-database-needed.html": "데이터베이스가 뭔가요 — 도서관과 마법 상자",
  "database-history-sql-nosql.html": "데이터베이스는 왜 종류가 많을까 — SQL과 NoSQL의 역사",
  "sql-basics-and-table-design.html": "SQL 구경하기 — 표, 관계, 그리고 빠른 이유",
  "transactions-normalization-nosql-types.html": "트랜잭션, 정규화, 그리고 NoSQL 네 가지",
  "user-accounts-sessions-and-cache.html": "회원가입과 로그인을 데이터로 보면",
  "sql-injection-and-backup-basics.html": "Little Bobby Tables — SQL 주입과 백업",
  "choosing-a-free-database.html": "무료로 쓸 수 있는 데이터베이스 고르기",
  "domain-expertise-ai-era-asset.html": "도메인 전문성이 AI 시대의 약점이 아니라 자산인 이유",
  "ai-poc-and-application-judgment.html": "도구에서 시작하면 아무도 안 씁니다 — 업무 적용 판단과 PoC",
  "computational-thinking-for-prompting.html": "컴퓨팅 사고법 — 큰 문제를 AI가 풀 수 있는 조각으로",
  "mainquest-mvp-and-doom-loop.html": "MVP는 완벽이 아니라 하나는 끝까지 되는 것 — 메인 퀘스트 착수기",
  "what-is-prompt-engineering.html": "프롬프트 엔지니어링이란? (1)",
  "what-is-ai-agent.html": "AI 에이전트(Agent)란 무엇인가 (2)",
  "what-is-model-input.html": "AI가 실제로 읽는 입력이란? (3)",
  "context-engineering-basics.html": "컨텍스트 엔지니어링이란? (4)",
  "prompt-engineering-history.html": "프롬프트 기법의 역사 (5)",
  "prompt-technique-verification.html": "프롬프트 기법 재검증하기 (6)",
  "agent-self-improvement-complexity.html": "AI 에이전트 자기개선과 복잡도 (7)",
  "ai-agent-beginner-guide.html": "AI 에이전트(Agent) 쉽게 이해하기",
  "prompt-execution-three-paths.html": "프롬프트 세 경로 직접 실행해보기 — Claude SDK·LangChain·Ollama",
  "agent-react-loop-and-autogpt.html": "에이전트의 ReAct 루프와 AutoGPT 소동",
  "mcp-usb-c-for-ai.html": "MCP — AI를 내 데이터에 꽂는 USB-C",
  "ai-skills-and-rules-files.html": "스킬과 규칙 파일 — 반복 작업을 AI에게 외워 두기",
  "ai-permissions-local-models-and-token-cost.html": "AI에게 컴퓨터를 맡길 때 — 권한, 로컬 모델, 토큰 비용",
  "choosing-ai-coding-tools.html": "AI 코딩 도구 고르기 — 터미널이냐 편집기냐 클라우드냐",
  "claude-plugins-and-spec-driven-development.html": "플러그인과 명세 주도 개발",
  "compound-engineering-and-loop-engineering.html": "컴파운드 엔지니어링과 루프, MCP 다음은 CLI",
  "opencode-models-and-muse-spark.html": "모델 이름이 왜 이렇게 많을까 — opencode 모델 고르기와 Muse Spark 1.3 (1)",
  "opencode-sisyphus-orchestration.html": "혼자 일하던 에이전트를 팀으로 — Sisyphus와 오케스트레이션 플러그인 (2)",
  "what-is-automation-workflow-agent.html": "자동화·워크플로·에이전트, 뭐가 다를까 (1)",
  "n8n-agent-delegation-and-if-node.html": "코딩 에이전트에게 흐름을 맡기고, IF 노드로 갈림길 만들기 (2)",
  "n8n-self-hosting-options.html": "n8n 직접 띄워보기 — 셀프 호스팅, 어디까지 내 책임일까 (3)",
  "reading-python-code-basics.html": "파이썬 코드 눈으로 읽기 — 함수·변수·반복·오류·async",
  "how-ai-learns-from-data.html": "AI는 어떻게 '배울까' — 규칙에서 데이터로",
  "turning-data-into-numbers.html": "데이터를 숫자로 바꾸기 — 벡터와 텐서",
  "smallest-learning-in-code.html": "가장 작은 학습을 코드로 보기 — 카페 매출 예측",
  "softmax-and-mnist-classification.html": "softmax로 분류하기 — MNIST 실습",
  "confusion-matrix-and-metrics.html": "맞혔다는 말로는 부족하다 — 혼동 행렬과 정확도·정밀도·재현율",
  "fine-tuning-and-transfer-learning.html": "남이 배운 것을 물려받다 — 파인튜닝",
  "why-gpu-and-colab-cli.html": "왜 내 노트북으론 벅찰까 — GPU와 Colab CLI",
  "how-cnn-broke-the-depth-wall.html": "지금 이 모델은 어디서 왔을까 — 이미지가 먼저 연 길",
  "how-language-broke-the-order-wall.html": "언어가 부딪힌 순서의 벽 — RNN에서 어텐션까지",
  "birth-of-the-transformer.html": "트랜스포머의 탄생 — Q/K/V와 두 길의 합류",
  "pretraining-and-scaling-laws.html": "사전학습과 스케일링 — GPT는 어떻게 커졌나",
  "what-is-alignment-sft-rlhf-dpo.html": "정렬이란 무엇인가 — SFT, RLHF, DPO",
  "transformers-beyond-language.html": "트랜스포머가 언어 밖으로 — ViT, Whisper",
  "tokens-and-context-window-cost.html": "토큰과 컨텍스트 — 활용가가 보는 비용과 한계",
  "training-vs-inference-memory.html": "내 노트북에서도 LLM이 돌아갈까",
  "quantization-why-it-still-works.html": "양자화 — 정밀도를 깎아도 왜 멀쩡할까",
  "kv-cache-and-vram-budget.html": "KV 캐시와 VRAM — 내 컴퓨터에 들어갈지 계산",
  "running-local-llm-with-ollama.html": "직접 Ollama로 로컬 LLM 돌려보기",
  "three-ways-to-run-an-llm.html": "로컬이냐 API냐는 틀린 질문 — 세 갈래",
  "where-does-your-data-stay.html": "데이터는 어디에 남는가",
  "cost-and-control-of-local-llm.html": "비용과 통제권 — 손익분기 계산과 누가 바꾸는가",
  "value-vs-location-two-requests.html": "금요일 오후에 도착한 두 개의 요청",
  "why-cant-ai-read-this-pdf.html": "PDF인데 왜 AI가 못 읽나요 — OCR의 역사",
  "ocr-assembly-line-and-error-propagation.html": "글자를 찾고 읽는 조립 라인",
  "object-detection-and-iou.html": "물체 찾기와 IoU — 탐지 결과를 믿는 법",
  "segmentation-and-sam.html": "박스로 안 되는 일 — 분할과 SAM",
  "vision-language-models.html": "이미지와 언어를 함께 보는 모델 — VLM",
  "choosing-ai-tools-and-yolo-practice.html": "AI 도구 선택 상담법, 그리고 YOLO 실습",
  "outsourced-labor-kept-decisions.html": "넘긴 것은 노동이고 남은 것은 결정입니다",
  "blank-slots-model-decides.html": "같은 모델인데 결과가 갈립니다",
  "gan-to-diffusion-models.html": "노이즈에서 되돌린다는 발상 — GAN에서 확산 모델까지",
  "latent-diffusion-and-distillation.html": "개인 컴퓨터로 내려온 날 — 잠재 확산과 증류",
  "writing-image-prompts.html": "프롬프트를 쓰는 법 — 여섯 칸과 재질 하나",
  "automating-image-generation.html": "코드로 이미지 생성 자동화하기",
  "choosing-image-generation-tools.html": "무엇으로 만들 것인가 — 라이선스, ControlNet",
  "video-generation-and-empty-slots.html": "동영상도 만들 수 있을까 — 빈 칸은 중립이 아니다",
  "why-multimodal-one-model.html": "왜 한 모델에 다 넣으려 하나 — 모달리티라는 말",
  "clip-and-vision-language-models.html": "픽셀을 문장처럼 다룬다는 발상 — CLIP과 VLM",
  "speech-to-text-history.html": "소리를 글자로 바꾸는 길 — STT 반백년의 계보",
  "choosing-a-local-whisper.html": "내 노트북에서 돌아가는 것 고르기 — Whisper",
  "omni-models-and-inference-engines.html": "옴니 모델과 그걸 돌리는 엔진",
  "choosing-a-voice-synthesis-tool.html": "같은 \"오픈소스\"가 아니다 — 목소리 합성기",
  "voice-cloning-and-responsible-ai.html": "그 목소리, 복제해도 됩니까",
  "why-photos-lose-distance.html": "셔터가 닫힐 때 사라지는 것",
  "four-containers-for-3d-space.html": "공간을 담는 네 가지 그릇",
  "birth-of-nerf-and-gaussian-splatting.html": "장면을 외우게 하다 — NeRF와 스플래팅",
  "recovering-depth-from-photos.html": "사진에서 거리를 되찾는 법",
  "turning-points-into-splats.html": "점을 알갱이로 바꾸는 계산",
  "shrinking-splat-files-for-the-web.html": "파일을 줄이고 화면에 그리기",
  "thirty-years-of-3d-reconstruction.html": "서른 해 동안 난 길들 — 3차원 복원사",
  "judging-and-fixing-a-3d-scan.html": "안 될 때와 더 낫게 — 스캔 판단법",
  "famous-is-not-the-same-as-usable.html": "유명한 것과 쓸 수 있는 것은 다르다",
  "same-week-different-fields.html": "같은 주에 다른 데서 벌어진 일들",
  "foundation-models-for-tables.html": "학습 없이 표를 읽는 모델",
  "from-sequence-to-structure.html": "서열을 읽던 모델이 간 곳",
  "designing-proteins-backwards.html": "방향을 뒤집다 — 없던 단백질을 짓는 법",
  "new-molecules-new-crystals.html": "없던 분자와 없던 결정",
  "graphs-and-interatomic-forces.html": "점과 선으로 보는 세계 — 그래프 신경망",
  "learning-the-weather-instead-of-computing-it.html": "슈퍼컴퓨터가 하던 일을 배우다",
  "a-model-with-a-body.html": "몸을 얻은 모델",
  "rewards-where-grading-is-possible.html": "채점이 되는 곳에 걸리는 보상",
  "open-versus-usable-today.html": "공개된 것과 오늘 쓸 수 있는 것",
  "knowing-where-not-to-go-is-also-a-map.html": "안 갈 데를 아는 것도 지도입니다",
  "instruction-design-basics.html": "지시 설계란 무엇인가 (1)",
  "instruction-priority-and-testing.html": "지시 우선권과 검증 (2)",
  "output-format-and-metrics.html": "답의 모양과 채점법 (3)",
  "instruction-failure-types.html": "지시 실패, 진단하고 고치기 (4)",
  "instruction-design-principles.html": "지시 설계 원칙 정리 (5)",
  "eleven-ways-same-question.html": "같은 질문, 열한 가지 방법 — 로컬 모델로 직접 재보기",
  "why-instructions-work-training-lineage.html": "왜 지시를 따르는가 — SFT·RLHF·DPO·GRPO의 계보",
  "context-window-budget.html": "컨텍스트 창은 왜 유한한가 (1)",
  "lost-in-the-middle-and-context-rot.html": "길게 넣어도 안 읽힐 수 있다 (2)",
  "context-strategy-and-rag.html": "무엇을 넣을지 정하는 법 — RAG (3)",
  "context-experiment-and-injection-defense.html": "같은 질문, 다른 맥락 (4)",
  "agents-md-and-cache-economics.html": "AGENTS.md와 캐싱 경제학 (5)",
  "agent-tool-design-and-harness.html": "에이전트가 도구를 쥔다는 것 — 모델·하네스·루프 (1)",
  "tool-contract-and-schema.html": "도구를 실제로 설계하기 — 정의서·스키마·MCP 실습 (2)",
  "tool-permission-and-evaluation.html": "안전하게 쓰고 평가하기 — 권한·회귀·과제 제출 (3)",
  "rag-chatbot-project-overview.html": "근거를 보여주는 챗봇 만들기 — 프로젝트 개관 (1)",
  "rag-chatbot-prd-questions.html": "바이브 코딩의 첫 문장 — PRD를 스스로에게 묻기 (2)",
  "rag-chatbot-chunk-design.html": "검색되는 자료와 답할 수 있는 자료는 다르다 — 청크 설계 (3)",
  "rag-chatbot-embedding-vectorstore.html": "브라우저 안에서 문장을 좌표로 바꾸기 — 임베딩과 벡터스토어 (4)",
  "rag-chatbot-hybrid-search.html": "가까운 청크를 고른다 — 코사인과 BM25의 하이브리드 검색 (5)",
  "rag-chatbot-prompt-streaming.html": "프롬프트는 근거의 경계다 — 프롬프트 조립과 로컬 LLM 스트리밍 (6)",
  "rag-chatbot-llm-judge.html": "답변 뒤에 심사위원 하나를 더 둔다 — LLM-as-a-Judge (7)",
  "rag-chatbot-prompt-experiment.html": "감이 아니라 기록으로 — 나만의 루브릭으로 실험하기 (8)",
  "rag-chatbot-submission.html": "지도를 접고 첫걸음을 — 배포와 제출 (9)",
  "mcp-skill-tool-call-anatomy.html": "도구 하나가 호출되기까지 — 정의·파싱·구조화 요청 (1)",
  "mcp-skill-protocol-roles.html": "호스트·클라이언트·서버가 나누는 대화 — MCP 연결 구조와 메시지 (2)",
  "mcp-skill-building-server.html": "업무 기록 서버 직접 만들기 — uv 환경과 Python MCP 서버 (3)",
  "mcp-skill-host-connection.html": "호스트에 연결하고 첫 도구 호출 확인하기 (4)",
  "mcp-skill-context-and-search.html": "도구가 많아지면 생기는 문맥 부담 — Tool Search와 Code Mode (5)",
  "mcp-skill-why-skill-needed.html": "같은 기록, 다른 판정 — Skill이 필요한 이유 (6)",
  "mcp-skill-first-weekly-report.html": "팀 규칙으로 첫 주간보고서 쓰기 (7)",
  "mcp-skill-writing-skill-md.html": "완성한 판단을 SKILL.md로 남기기 (8)",
  "mcp-skill-reuse-verification.html": "다음 주에도 통하는가 — Skill 재사용 검증하기 (9)",
  "mcp-skill-colab-notebook.html": "계산 과정을 노트북에 남기기 — Colab MCP 연결 (10)",
  "mcp-skill-google-oauth-setup.html": "내 표를 읽는 프로그램 만들기 — Google OAuth 준비 (11)",
  "mcp-skill-google-sheets-mcp.html": "로그인부터 표가 반환되기까지 — 인증 코드와 MCP 서버 (12)",
  "mcp-skill-adapting-to-my-task.html": "내 업무에 맞게 바꿔보기 — 데이터·기준·기능 나누기 (13)",
  "mcp-skill-wikiskill-research.html": "에이전트도 경험을 쌓는다 — WikiSkill 연구가 보는 Skill (14)",
  "langgraph-what-and-why.html": "다음에 어느 코드가 실행될까 — LangGraph와 워크플로·에이전트 (1)",
  "langgraph-state-node-edge.html": "흐름을 그림으로 짠다 — LangGraph의 State·Node·Edge (2)",
  "langgraph-branch-drills.html": "갈림길을 밀어붙인다 — 세 갈래·라벨·끝나지 않는 반복 (3)",
  "langgraph-branches-and-tool-loop.html": "모델이 다음 길을 고르게 한다 — 도구를 쥐여 주는 루프 (4)",
  "langgraph-env-troubleshooting.html": ".env가 안 읽혔던 네 겹의 이유 — 원격 주피터에서 API 키 넣기 (5)",
  "langgraph-pattern-chaining.html": "① 프롬프트 체이닝 — 순서대로, 사이에 검사 (6)",
  "langgraph-pattern-routing.html": "② 라우팅 — 먼저 분류하고, 한 갈래로 (7)",
  "langgraph-pattern-parallelization.html": "③ 병렬화 — 동시에 돌리고, 합친다 (8)",
  "langgraph-pattern-orchestrator-worker.html": "④ 오케스트레이터-워커 — 몇 갈래일지 LLM이 정한다 (9)",
  "langgraph-pattern-evaluator-optimizer.html": "⑤ 평가자-최적화자 — 통과할 때까지 고쳐 쓰기 (10)",
  "newsletter-agent-skeleton.html": "뉴스레터 에이전트를 빈 노드 다섯 개로 먼저 세운다 (11)",
  "newsletter-agent-collect.html": "기사를 어디서 가져올까 — RSS·관문·수집 노드 (12)",
  "newsletter-agent-select.html": "100건에서 5건 고르기 — 점수 대신 비교, 예선과 본선 (13)",
  "newsletter-agent-summarize-verify.html": "요약을 세 칸으로 받고 원문과 대조한다 (14)",
  "newsletter-agent-publish-schedule.html": "디스코드로 매일 아침 받아 보기 — 웹훅과 GitHub Actions (15)",
  "newsletter-agent-metrics-config.html": "돌고 나서 재 본다 — 실행 기록과 설정 파일 (16)",
  "cs-agent-routing-eval.html": "문의 한 줄을 다섯 갈래로 — 라우트는 회사 문서에서 가져온다 (17)",
  "cs-agent-grounding.html": "값을 말하지 말고 조회하게 한다 — 매뉴얼 쪼개기·도구·가드레일 (18)",
  "cs-agent-improve.html": "59%에서 94%로 — 프롬프트만 고쳐 지표를 올린 기록 (19)",
  "graphrag-why-multihop.html": "검색으로는 못 찾는 답 — 멀티홉 질문과 지식 그래프 (20)",
  "graphrag-build-knowledge-graph.html": "스키마가 답할 질문을 정한다 — 추출·정규화·위키 분류 (21)",
  "graphrag-agent-three-routes.html": "세 갈래로 답하는 에이전트 — 커뮤니티 요약·라우터·탐색 예산 (22)",
  "graphrag-goldenset-eval.html": "같은 15문항으로 채점한다 — 세 층 평가와 심판의 한계 (23)",
  "multi-agent-split-gains-and-losses.html": "나누면 좋아질까 — 멀티 에이전트의 득실과 판정표 (1)",
  "multi-agent-four-structures.html": "여럿이라는 말만으론 부족하다 — 네 가지 구조와 맞는 과업 (2)",
  "multi-agent-three-runs-abc.html": "같은 버그를 세 방식으로 — 기준선·워크플로·오케스트레이션 실행 (3)",
  "multi-agent-judging-records.html": "통과했다는 말로는 부족하다 — 두 층 채점과 채택·축소·폐기 판정 (4)",
  "multi-agent-ecosystem-tools.html": "실험이 남긴 네 문제와 도구들 — Agent Teams·Workflows·oh-my-claudecode·herdr (5)",
  "openclaw-what-and-where-from.html": "새 껍데기, 같은 바닷가재 — OpenClaw는 무엇이고 어디서 왔나 (1)",
  "openclaw-install-and-first-chat.html": "연습 폴더에 들이기 — 설치·온보딩·첫 대화 (2)",
  "openclaw-session-records-and-usage.html": "답변이 아니라 흔적을 본다 — 세션 기록과 사용량 (3)",
  "openclaw-telegram-channel-and-pairing.html": "폰에서 부리기 — 텔레그램 채널과 페어링 (4)",
  "openclaw-security-boundaries.html": "어디까지 해도 되는가 — 권한 모드·입구·인젝션·공개 권고 (5)",
  "openclaw-multi-agent-bindings.html": "한 게이트웨이에 여러 역할 — 바인딩·델리게이트·스탠딩 오더 (6)",
  "openclaw-automations-scheduling.html": "사람이 기억하지 않도록 — 자동화 예약과 cron (7)",
  "openclaw-pi-core-and-extensions.html": "뼈대와 손 — pi 코어와 확장 기능 투어 (8)",
  "harness-observation-and-feature-map.html": "맡길 일부터 관찰까지 — 하네스 보는 법 (1)",
  "harness-action-format-and-context.html": "행동을 좁히고 문맥을 고른다 — 행동 포맷과 컨텍스트 관리 (2)",
  "harness-experience-and-reflection.html": "성공은 자산으로, 실패는 설명으로 — 경험·스킬 축적과 반성 (3)",
  "harness-minimal-and-permission.html": "덜어내기와 경계 긋기 — 미니멀과 권한·보안 (4)",
  "harness-evaluation-and-comparison.html": "결과와 궤적을 함께 본다 — 평가 루프와 일곱 하네스 비교 (5)",
  "harness-hypothesis-experiment.html": "내 불편을 가설로 — 개선 실험 설계와 제출 (6)",
  "my-harness-users-and-prd.html": "맡길 일부터 적는다 — 내 하네스의 사용자와 미완성 PRD (1)",
  "my-harness-platform-and-provider.html": "어디서 돌리고 무엇에 연결할까 — 플랫폼·언어·모델 제공자 (2)",
  "my-harness-flow-and-state.html": "끝날 때까지 따라가기 — 실행 흐름·상태·승인과 종료 조건 (3)",
  "my-harness-interfaces.html": "버튼 하나 뒤의 약속 — API와 도구 인터페이스 (4)",
  "my-harness-acceptance.html": "만들기 전에 합격선을 긋는다 — 완료 조건과 검증 시나리오 (5)",
  "my-harness-vertical-slice.html": "얇게 한 번 관통시키기 — 첫 구현과 막힌 지점 찾기 (6)",
  "my-harness-python-code-reading.html": "설계가 코드 어디에 앉는가 — 실행 가능한 Python 하네스 읽기 (7)",
  "my-harness-benchmark-local-port.html": "남이 낸 문제로 재보기 — 벤치마크 10문항 로컬 평가 (8)",
  "my-harness-scoring-and-report.html": "분모를 지키는 정직 — 점수 읽기·비교 실험·제출 (9)",
  "generative-ai-design-patterns-ch1.html": "프롬프트에서 에이전트까지 — 1장 정리노트",
  "generative-ai-design-patterns-ch2.html": "신입사원의 말투를 붙잡다 — 2장 정리노트",
  "generative-ai-design-patterns-ch3.html": "다 외우지 말고, RAG로 찾아보게 하자 — 3장 정리노트",
  "codeact-code-as-agent-actions.html": "실행 가능한 코드 행동이 더 나은 LLM 에이전트를 만든다 (2024.02.01)"
 }
};
