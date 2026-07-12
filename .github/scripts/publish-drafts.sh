#!/usr/bin/env bash
set -euo pipefail

TODAY=$(date -u +%Y-%m-%d)
CHANGED=0

if [ -d _drafts ]; then
  while IFS= read -r -d '' file; do
    publish_date=$(sed -n 's/.*<!-- publish-date: \([0-9-]*\) -->.*/\1/p' "$file" | head -n1)
    if [ -z "$publish_date" ]; then
      echo "건너뜀 (발행일 없음): $file"
      continue
    fi
    if [[ "$publish_date" < "$TODAY" || "$publish_date" == "$TODAY" ]]; then
      dest="${file#_drafts/}"
      mkdir -p "$(dirname "$dest")"
      sed '/<!-- publish-date:/d' "$file" > "$dest"
      rm "$file"
      echo "발행됨: $dest (예약일: $publish_date)"
      CHANGED=1
    else
      echo "아직 발행일 아님: $file (예약일: $publish_date, 오늘: $TODAY)"
    fi
  done < <(find _drafts -type f -name "*.html" -print0)
fi

if [ "$CHANGED" = "1" ]; then
  git config user.name "github-actions[bot]"
  git config user.email "github-actions[bot]@users.noreply.github.com"
  git add -A
  git commit -m "예약 발행 자동화: $TODAY"
  git push
else
  echo "발행할 예약 글이 없습니다."
fi
