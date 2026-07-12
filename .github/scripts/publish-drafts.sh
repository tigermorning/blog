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

git add -A
git commit -m "예약 발행: $dest"
git push

echo "발행됨: $dest"
