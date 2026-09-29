# HANDOFF — 전 글 점검·수정 (WRAP UP 과제 기준)

기존 `HANDOFF.md`(hcom·세션 연계)와 별개 갈래. 이 문서만 보고 시작할 수 있게 적었다.

다음 사람이 칠 첫 명령:

```bash
git status --short --branch && node scripts/audit-posts.mjs | head -40
```

---

## 목표

- `ko/` 아래 **발행된 모든 글**을 아래 4가지 기준으로 점검하고 고친다
- **새 WRAP UP 글은 쓰지 않는다** (사용자 지시, 2026-09-29)
- 출처: 모두의연구소 노션 "에이전트 팀 꾸리기 WRAP UP!" 페이지
  - URL: `https://app.notion.com/p/WRAP-UP-3ea8820152dc80f69315ccff2ed7674f` (크롬 로그인 세션으로 열림)

### 기준 4가지 (노션 "블로그 작성 시 주의할 점" 원문)

| # | 원문 | 이 블로그에서의 판정 방법 |
|---|---|---|
| 1 | 독자를 고려하고 작성하자 | 첫 화면에 "누구를 위한 글인지·읽기 전에 알아야 할 것"이 있는가. 용어가 처음 나올 때 풀이가 있는가 |
| 2 | 너무 길거나 짧게 작성하지 말자 | 같은 시리즈 형제 글과 비교해 튀는가 (아래 수치 참고) |
| 3 | 단순 정보 나열식은 필요 없다 | 사실 목록만 있고 "왜·언제 쓰나·나쁜 선택 vs 좋은 선택"이 없는 구간이 있는가 |
| 4 | 줄글로만 되어 있으면 재미없다 | 표·그림·박스 없이 문단만 이어지는 구간이 있는가 |

- 이 기준은 이미 블로그 규칙과 대부분 겹침 → **새 규칙을 만들지 말고 기존 규칙으로 판정**
  - `tigermorning-blog-post` 스킬의 "요약 노트 7규칙" (한 줄 정의 → 읽기 전에 박스 → 비유+대비표 → 흐름 그림 → 나쁜/좋은 선택 → 수치 표 → 용어 각주)
  - 메모리의 blog 관련 feedback 전부 (`MEMORY.md`에서 `Blog`·`blog` 항목)

---

## 현재 상태 (측정 2026-09-29, `node scripts/audit-posts.mjs`)

| 항목 | 값 |
|---|---|
| 측정 대상 | `ko/*.html` 250편 (목록 페이지 6개 제외) |
| 암호 글 (`<main>` 없음) | 7편 — **손대지 말 것**. 아래 gotcha |
| 점검 대상 | 243편 |
| 본문 글자 수 | p10 4,554 · 중앙값 6,642 · p90 15,739 · 최대 30,499 |
| 중앙값의 2배 초과 | 40편 (최상위: `newsletter-agent-*` 5편 26k~30k, `mcp-skill-google-sheets-mcp` 24k, `graphrag-why-multihop` 23k) |
| 중앙값의 0.3배 미만 | 1편 (`hello-world.html`, 65자 — 테스트 페이지, 대상 아님) |
| 문단 연속(`maxRun`) ≥ 6 | 38편 |
| 문단 연속 ≥ 4 | 236편 — 기준으로 쓰기엔 너무 넓음 |
| 시각 요소 ≤ 3 | 1편 |
| 점검·수정 완료 | 0편 |

- 수치의 한계 (가정 아님, 스크립트 동작):
  - `maxRun`은 `<h2>/<h3>`에서도 끊김 → 소제목만 끼고 줄글이 이어지는 구간은 못 잡음
  - `visuals`는 `<ul>`도 셈 → 불릿만 많은 "정보 나열"은 오히려 점수가 좋게 나옴 (기준 3은 숫자로 못 잼, 읽어서 판정)
  - 길이는 시리즈마다 적정치가 다름. 전체 중앙값이 아니라 **같은 시리즈 형제 글**과 비교할 것

### 수정 대상이 아닌 파일

| 파일 | 이유 |
|---|---|
| `generative-ai-design-patterns-ch1(-review)`, `ch2(-review)`, `ch3`, `study-attention-transformer`, `study-evaluation-metrics` | 암호 글 |
| `hello-world.html`, `en/`, `zh/` | 테스트·언어 스텁 |
| `posts.html`, `start.html`, `topic-map.html`, `big-map.html`, `_sidebar.html`, `index.html` | 목록·이동 페이지 (글 제목이 바뀌면 여기만 동기화) |
| `_drafts/` | 발행 안 된 초안 (이미지 폴더·JSON·검증 스크립트뿐, 글 없음) |

---

## 완료

1. 노션 과제 페이지 읽음 — 과제 옵션(정리/확장/활용)과 주의점 4가지 확인
2. 사용자에게 범위 확인 → "WRAP UP 글은 안 씀, 전편 점검·수정, 새 세션에서 진행"
3. `scripts/audit-posts.mjs` 작성·실행 — 위 표의 수치 산출

---

## 남은 일

1. **작업 시작 전 다른 세션 미커밋 파일 처리 확인**
   - 2026-09-29 시점 다른 세션이 건드린 파일: `ko/_sidebar.html`, `ko/posts.html`, `ko/hapseok16-ai-talk-fact-check.html`, `ko/yuval-harari-ai-agent-interview.html`, `search-data.js`, `style.css`, 새 글 `ko/hapseok-two-talks-insight.html`, `ko/hapseok10-ai-economy-talk.html`, `ko/hapseok16-ai-talk-flow.html`
   - 착수: `git status --short`. 아직 dirty면 사용자에게 먼저 커밋할지 묻고, 그 파일들은 마지막 배치로 미룸
2. **판정 기준 확정 (1배치 시범 후)**
   - 착수: 시리즈 하나(예: `newsletter-agent-*` 6편)를 골라 기준 1~4로 판정표를 만들고, 수정 전후를 사용자에게 보여 합의
   - 합의된 판정 예시를 이 문서 "판정 예시" 절에 추가
3. **시리즈 단위 배치 수정**
   - 순서: `posts.html` 단계 순서(1단계부터). 한 배치 = 한 시리즈 또는 10편 이하
   - 배치마다: 수정 → `node scripts/build-search-data.mjs` → 브라우저 확인 → 커밋 1개
   - 진행 상황은 아래 "진행 표"에 파일명 단위로 기록
4. **길이 이상치 40편**: 쪼갤지(메모리 `Blog Post Granularity`) 줄일지 사용자 판단 필요 — 목록만 뽑아 묻기

### 진행 표

| 배치 | 파일 | 기준 위반 | 조치 | 커밋 |
|---|---|---|---|---|
| (비어 있음) | | | | |

---

## 파일

| 파일 | 용도 | 명령 |
|---|---|---|
| `scripts/audit-posts.mjs` | 길이·시각 요소·줄글 연속 수치 (후보 고르기용, 판정 아님) | `node scripts/audit-posts.mjs` / `--csv` |
| `scripts/build-search-data.mjs` | 글 수정 후 검색 데이터 재생성 | `node scripts/build-search-data.mjs` |
| `ko/posts.html` | 8단계 사다리 목록, prev/next 체인의 기준 | — |
| `FEATURE_MAP.md` | 블로그 UI 조작법 | — |

---

## 주의 (gotcha)

- **암호 글 7편은 열지도 말 것.** 수정이 필요하면 메모리 `No Password In Chat` 절차(로컬 복호화 스크립트)로만, 비밀번호는 채팅에 묻지 않음
- **기준 4개를 "새 섹션 추가"로 해결하지 말 것.** 메모리 `Clarify Without Bloat`: 빠진 것만 채우고 길이를 늘리지 않음. 줄글→표 전환은 같은 내용을 형태만 바꾸는 것
- **글에 "이번에 규칙을 바꿨다" 같은 메타 문장을 넣지 말 것.** 메모리 `No Meta Narration`
- **숫자·실행 결과를 새로 쓰면 실제로 돌려서 확인할 것.** 메모리 `No Unverified Output Claims`
- **1인칭 일화를 지어내지 말 것.** 메모리 `Grounded First-Person Lines`
- **글을 합칠 때 원본 내용을 지우지 말 것.** 메모리 `Merge Keeps Originals`
- **한 커밋에 수십 편을 넣지 말 것.** 배치별 커밋이라야 되돌릴 수 있음
- **다른 세션 파일을 같이 커밋하지 말 것.** `git add`는 파일명을 지정. 메모리 `Multi-Session Repo Hygiene`
- **수정 후 `build-search-data.mjs`를 반드시 다시 돌릴 것.** 안 돌리면 검색 결과가 옛 본문을 보여 줌
- **라이브 사이트 404는 정상.** 확인은 로컬 파일로 (메모리 `Blog Site 404 Intended`)
