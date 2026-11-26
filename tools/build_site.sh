#!/bin/sh
# Build the site.   tools/build_site.sh production   -> site/          (https://ponoor.com/docs/step-series/)
#                   tools/build_site.sh preview      -> site-preview/  (https://ponoor.com/docs-preview/step-series/, noindex)
# generate.py (pages made from the spec, llms.txt) runs first, then mkdocs build --strict --clean.
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"
case "${1:-}" in
    production) config=mkdocs.yml ;;
    preview) config=mkdocs.preview.yml ;;
    *) echo "usage: tools/build_site.sh production|preview" >&2; exit 2 ;;
esac
py=python3
python3 -c "import yaml" >/dev/null 2>&1 || py=python
[ -x .venv/bin/python ] && py=.venv/bin/python
mk="$py -m mkdocs"
"$py" tools/generate.py --defaults both --coverage
$mk build --strict --clean -f "$config"
