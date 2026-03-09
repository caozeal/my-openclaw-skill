#!/bin/bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: ./skills/wechat-markdown-publisher/scripts/preview_wechat.sh <input.md> [theme]" >&2
  exit 1
fi

INPUT="$1"
THEME="${2:-janus}"
OUTPUT="${INPUT%.*}.wechat.html"

python3 ./skills/wechat-markdown-publisher/scripts/md_to_wechat.py "$INPUT" --theme "$THEME" --output "$OUTPUT"

if command -v open >/dev/null 2>&1; then
  open "$OUTPUT"
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$OUTPUT"
else
  echo "Preview file generated: $OUTPUT"
fi
