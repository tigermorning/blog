# HANDOFF

세션이 바뀌어도 같은 조사를 다시 하지 않기 위한 인수인계 문서. 이 저장소에서 진행 중인 작업의 **상태**를 적는다.

다음 사람이 칠 첫 명령:

```bash
hcom status
```

---

## 목표

- 이 저장소는 GitHub Pages 블로그(`tigermorning.github.io`)
- 이 문서가 다루는 갈래: **세션 간 연계** — 여러 Claude 세션·워크트리가 같은 저장소를 건드릴 때 서로의 진행 상황을 파악하는 문제
- 블로그 글 자체의 작업 규칙은 이 문서가 아니라 `tigermorning-blog-post` 스킬과 `MEMORY.md`에 있음

---

## 현재 상태

| 항목 | 상태 | 근거 (측정 2026-09-16) |
|---|---|---|
| hcom | 0.7.25 설치됨 | `uv tool install hcom`. 실행 파일 `C:\Users\user\.local\bin\hcom.exe` |
| Claude 훅 | 설치됨 | `C:\Users\user\.claude\settings.json` |
| OpenCode 훅 | 설치됨 | `C:\Users\user\.config\opencode\plugins\hcom.ts` |
| 전역 `notes` | 설정됨 | request 받으면 `hcom send`로 답하라는 규율. `hcom config notes`로 확인 |
| `opencode_args` | **비워 둠** | 값을 넣으면 죽음. 아래 gotcha 참조 |
| 실행 중 에이전트 | 없음 | 테스트용 `kira`/`luna`/`toku` 전부 종료 |
| hcom relay | 미설정·미검증 | 이 세션에서 안 씀 |

---

## 완료 (측정값 포함)

1. **hcom 설치·훅 연결** — Claude, OpenCode 양쪽. `hcom status`에서 둘 다 `installed`
2. **Claude ↔ OpenCode 왕복 성공** — `muse → kira(Claude) → luna(OpenCode) → kira → muse`, 23초
   - 증거: 이벤트 `#49` `{"from":"luna","intent":"ack","reply_to_local":44,"text":"ko/*.html: 232 top-level HTML files."}`
   - 숫자 독립 검증: `ls ko/*.html | wc -l` = 232
3. **첫 시도는 실패했음** — 최초 OpenCode 인스턴스(`silo`)는 자기 창에만 답하고 `hcom send`를 안 돌림
   - 증거: `#21 silo went idle without responding to your request #17`
   - 해결: 런치 시 시스템 프롬프트로 보고 규율 주입 + 전역 `notes` 설정
4. **워크트리 완료 보고 실험 통과** — 임시 워크트리에 hcom 에이전트를 띄우고, 사람 개입 없이 완료 보고 수신
   - 런치부터 보고까지 35초 (`02:14:31` launch → `02:15:06` message)
   - 보고 `완료: 803548b`를 git으로 독립 검증: 해당 브랜치에만 존재, 파일 1개 변경, main 무변동
   - 개입은 `hcom term`(읽기 전용 화면 보기) 1회뿐. 키 주입 없음
   - 실험 후 워크트리·브랜치 삭제 완료
5. **트랜스크립트 검색 한계 측정** — 아래 gotcha 1번의 근거
6. **`.gitignore`에 `.omc/*`, `.omo/` 추가** — `.omc/skills/`는 커밋 대상으로 남김
7. **블로그 글 발행** — `ko/hcom-connect-coding-agents.html` (hcom 소개). `posts.html`·`_sidebar.html`에 새 하위 카테고리 `#coding-tools`("바이브 코딩 도구") 신설해 배치
   - 앞으로 도구 기록은 이 하위 카테고리에 쌓음
   - 양방향 링크 연결: `multi-agent-ecosystem-tools.html`, `opencode-sisyphus-orchestration.html`
   - `node scripts/build-search-data.mjs` 재실행 완료 (227개 항목)
   - 목록 강조 규칙을 새로 만듦 — 아래 gotcha 참조

---

## 남은 일

1. **다른 저장소 핸드오프 0개** — `nk-briefing`, `python-study`, `english-lesson` 확인 결과 `.omc/handoffs` 없음
   - 착수: 각 저장소에서 `/oh-my-claudecode:handoff-notes`
2. **nk-briefing에 빈 워크트리 껍데기** — `.claude/worktrees/youthful-tu-321a39`가 항목 0개인 빈 디렉토리로 남음. 브랜치 `claude/youthful-tu-321a39`는 이미 삭제됨
   - 착수: `rm -rf` 후 `git worktree prune`
3. **사이드바 그룹 미정리** — 세션 약 100개 중 그룹 붙은 것 1개. 그 하나도 오분류(`english-lesson` 폴더 세션이 `Chinese-Lesson` 그룹에 들어감)
   - 우선순위 낮음. 검색 문제를 풀지 못함
4. **"작업 단위마다 커밋" 규칙 미적용** — 자식 세션이 커밋을 안 하면 부모가 git으로도 진행 상황을 못 봄

---

## 주의 (gotcha)

한 줄에 하나. 행동 지시형.

- **트랜스크립트 검색에 띄어쓴 구절을 쓰지 말 것.** 리터럴 부분 문자열 매칭이라 공백 포함 문자열이 원문에 그대로 있어야 히트함
  - 측정: `소스 선정` → 0건, `뉴스레터 소스 선정 기준` → 0건, `소스당` → **3건** (같은 내용)
  - 대신 쓸 것: 붙어 있는 희소 토큰 하나 (`DailyNK`, `Cloudflare 403`, `search-data.js`, `소스당`)
- **`opencode_args`에 hcom 런치 플래그를 넣지 말 것.** 툴 인자로 그대로 넘어가 OpenCode가 죽음
  - 측정: `--hcom-system-prompt`를 넣었더니 `exited 3s after spawn before binding (exit code 1)`
  - 대신 쓸 것: 런치 인라인 플래그 `hcom opencode --hcom-system-prompt '...'`, 또는 전역 `hcom config notes`
- **에이전트를 띄울 때 "보고 안 하면 실패로 간주"를 명시할 것.** 안 쓰면 자기 창에만 답하고 끝냄 (`silo` 사례)
- **워크트리 작업은 `hcom claude --dir <워크트리>`로 띄울 것.** 데스크톱 `spawn_task` 칩으로 뜬 세션은 hcom DB에 행이 없어 안 보임
- **완료 보고에 커밋 해시를 넣게 할 것.** 메시지를 믿지 말고 `git branch --contains <해시>`로 검증
- **새 셸에서 `hcom`을 못 찾으면 PATH를 넣을 것** — `export PATH="/c/Users/user/.local/bin:$PATH"`
- **`.omc/skills/`는 지우지 말 것.** `.gitignore`가 `.omc/*`를 막지만 이 폴더만 예외로 커밋 대상
- **`posts.html` 목록에서 이름을 강조할 때는 `<span class="name">`을 쓸 것.** 색은 그 `<li>`의 `--folder-accent`를 따라가므로 `<li style="--folder-accent:var(--folder-N);">`만 주면 됨. `<strong>`을 쓰면 `main strong`의 노란 형광펜이 걸려 다른 항목과 강조 방식이 어긋남
- **짧은 영문 소문자 이름에는 `name--chip`을 같이 줄 것** (`class="name name--chip"`). 색만으로는 덩어리가 안 생겨 긴 한글 제목 사이에서 묻힘. 긴 한글 이름에는 칩을 붙이지 않음
- **사이드바 하위 항목을 추가하면 `style.css`의 색 배정도 늘릴 것.** `.sidebar-tree > li:nth-of-type(2) .tree-subgroup:nth-child(N)`에 지정된 수만큼만 색이 붙고, 나머지는 대분류 탭 색을 그대로 물려받아 서로 구분이 안 됨
- **사이드바에는 `main` 안의 강조 규칙이 안 닿음.** 형광펜이 필요하면 `.tree-leaf-list .leaf-mark`를 쓰고, 세로 padding은 주지 말 것 — 16px 글자 상자가 이미 24px 줄 높이를 채워서 위아래 항목을 침범함

---

## 판단 (가정 — 재검증 대상)

측정이 아니라 이번 세션의 판단이다. 뒤집히면 이 절을 고칠 것.

- **실시간 세션 협업은 이미 해결됨.** 단 쓸 일이 드묾 — 세션 약 100개 조회 시 실행 중(`isRunning: true`)인 것이 하나도 없었음
- **시간차 인수인계는 근본 해결 불가.** 병목이 앱의 검색 구현이라 저장소 쪽에서 못 고침. 우회(= 이 문서 같은 파일)가 정답
- **워크트리 실험은 1회 시행.** 재현성 미확인
- **MEMORY.md가 현재 유일하게 작동하는 세션 간 채널.** 단 굳은 사실만 담고 진행 중 상태는 안 담음 — 그 빈자리를 이 문서가 맡음

---

## 파일

| 파일 | 용도 | 확인 명령 |
|---|---|---|
| `~/.hcom/config.toml` | hcom 전역 설정 (`notes`, `auto_approve` 등) | `hcom config` |
| `~/.claude/settings.json` | Claude 훅 (OMC 훅과 공존) | `hcom hooks` |
| `~/.config/opencode/plugins/hcom.ts` | OpenCode 훅 | `hcom hooks` |
| `.gitignore` | `.omc/*`, `.omo/` 제외 | `git status --short` |
| `MEMORY.md` | 세션 시작 시 자동 로드되는 굳은 사실 | — |

---

## 되돌리기

hcom을 걷어낼 때:

```bash
hcom hooks remove all
```

```bash
uv tool uninstall hcom
```
