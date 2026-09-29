#!/bin/sh
# Every local check of the site: structure and links, well-formed HTML, and each page served with 200.
# Run from anywhere: tools/check.sh
set -eu
cd "$(dirname "$0")/.."

python3 tools/check_site.py

pages=$(find . -name index.html -not -path './.git/*' | sort)
for page in $pages; do
    # Strict XML well-formedness catches unclosed or mismatched tags.
    xmllint --noout "$page"
    # The HTML parser of macOS's libxml2 doesn't know HTML5 elements; anything else it reports is a problem.
    problems=$(xmllint --html --noout "$page" 2>&1 \
        | grep 'parser error' \
        | grep -v -E 'Tag (header|nav|main|section|footer|details|summary|article) invalid' || true)
    if [ -n "$problems" ]; then echo "$problems"; exit 1; fi
done
echo "HTML well-formed."

port=8765
python3 -m http.server "$port" --bind 127.0.0.1 >/dev/null 2>&1 &
server=$!
trap 'kill "$server" 2>/dev/null' EXIT
sleep 1
for path in "" privacy/ terms/ feedback/ zh-hant/ zh-hant/privacy/ zh-hant/terms/ zh-hant/feedback/ \
            zh-hans/ zh-hans/privacy/ zh-hans/terms/ zh-hans/feedback/ styles.css feedback-form.js; do
    status=$(curl -s -o /dev/null -w '%{http_code}' "http://127.0.0.1:$port/$path")
    if [ "$status" != 200 ]; then echo "error: /$path returned $status" >&2; exit 1; fi
done
echo "Every page returns 200."
