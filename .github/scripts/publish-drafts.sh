#!/usr/bin/env bash
set -euo pipefail

QUEUE_FILE="_drafts/queue.txt"

if [ ! -f "$QUEUE_FILE" ] || [ ! -s "$QUEUE_FILE" ]; then
  echo "발행 대기열이 비어 있습니다."
  exit 0
fi

# 큐의 맨 앞 항목(다음 발행 대상) 가져오기
next_entry=$(head -n 1 "$QUEUE_FILE")

if [ -z "$next_entry" ]; then
  echo "발행 대기열이 비어 있습니다."
  exit 0
fi

# 낮 시간(KST 09:00~24:00)에만 발행. 그 전이면 이번 실행은 건너뜀
now_kst_hour=$(TZ=Asia/Seoul date +%-H)
if [ "$now_kst_hour" -lt 9 ]; then
  echo "KST 09시 이전이라 이번 실행은 건너뜁니다."
  exit 0
fi

# 남은 대기열 개수만큼 오늘 하루(남은 시간) 안에 다 발행되도록 간격을 계산.
# 간격은 최소 1시간, 대기열이 적을수록 하루 안에서 더 넓게 퍼짐.
queue_count=$(grep -c . "$QUEUE_FILE" || true)
now_kst_min=$(TZ=Asia/Seoul date +%-M)
minutes_left_today=$(( (24 - now_kst_hour) * 60 - now_kst_min ))
if [ "$minutes_left_today" -lt 60 ]; then
  minutes_left_today=60
fi
interval_sec=$(( minutes_left_today * 60 / queue_count ))
if [ "$interval_sec" -lt 3600 ]; then
  interval_sec=3600
fi

last_publish_ts=$(git log -1 --grep='^예약 발행: ' --format=%ct 2>/dev/null || echo 0)
now_ts=$(date +%s)
elapsed_sec=$(( now_ts - last_publish_ts ))

if [ "$last_publish_ts" -ne 0 ] && [ "$elapsed_sec" -lt "$interval_sec" ]; then
  echo "마지막 발행 후 $((elapsed_sec / 60))분 경과, 필요한 간격은 $((interval_sec / 60))분(대기열 ${queue_count}개 기준). 이번 실행은 건너뜁니다."
  exit 0
fi

src="_drafts/$next_entry"
dest="$next_entry"

git config user.name "github-actions[bot]"
git config user.email "github-actions[bot]@users.noreply.github.com"

if [ ! -f "$src" ]; then
  echo "경고: 큐에 있는 파일을 찾을 수 없습니다: $src (이 항목은 건너뜁니다)"
  tail -n +2 "$QUEUE_FILE" > "${QUEUE_FILE}.tmp" && mv "${QUEUE_FILE}.tmp" "$QUEUE_FILE"
  git add "$QUEUE_FILE"
  git commit -m "예약 발행: 대기열에서 누락된 항목 제거 ($next_entry)"
  git push
  exit 0
fi

mkdir -p "$(dirname "$dest")"
mv "$src" "$dest"

# 큐에서 맨 앞 줄 제거 (나머지는 다음 차례로 이월됨)
tail -n +2 "$QUEUE_FILE" > "${QUEUE_FILE}.tmp" && mv "${QUEUE_FILE}.tmp" "$QUEUE_FILE"

# sitemap.xml에 새로 발행된 글 주소 자동 추가
SITEMAP="sitemap.xml"
NEW_URL="https://tigermorning.github.io/blog/${dest}"
if [ -f "$SITEMAP" ] && ! grep -qF "$NEW_URL" "$SITEMAP"; then
  sed -i "s#</urlset>#  <url><loc>${NEW_URL}</loc></url>\n</urlset>#" "$SITEMAP"
  echo "sitemap.xml에 추가됨: $NEW_URL"
fi

# 랜딩 페이지(index.html)의 "최신 글" 링크를 방금 발행된 글로 자동 갱신
lang_dir="$(dirname "$dest")"
idx="$lang_dir/index.html"
if [ -f "$idx" ]; then
  post_title="$(grep -m1 -oP '(?<=<h1>)[^<]*' "$dest" || true)"
  if [ -n "$post_title" ]; then
    export POST_HREF="$(basename "$dest")"
    export POST_TITLE="$post_title"
    perl -0777 -pi -e '
      my $href = $ENV{POST_HREF};
      my $title = $ENV{POST_TITLE};
      s{(<a class="post-nav" href=")([^"]*)(">\s*<span class="post-nav-label">)([^<]*)(</span>\s*<span class="post-nav-title">)([^<]*)(</span>)}{$1.$href.$3.$4.$5.$title.$7}se;
    ' "$idx"
    echo "${idx} 최신 글 링크 갱신됨: ${POST_HREF}"
  fi
fi

git add -A
git commit -m "예약 발행: $dest"
git push

echo "발행됨: $dest"
