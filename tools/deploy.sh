#!/bin/sh
# Upload a built site to the server (ssh host "lolipop").
#
#   tools/deploy.sh preview              show what would be sent (--dry-run; nothing is written)
#   tools/deploy.sh production           the same for the real site
#   tools/deploy.sh preview --apply      really upload (only with --apply)
#   tools/deploy.sh production --apply
#
#   preview     site-preview/ -> lolipop:web/ponoor.com/docs-preview/step-series/   (https://ponoor.com/docs-preview/step-series/)
#   production  site/         -> lolipop:web/ponoor.com/docs/step-series/           (https://ponoor.com/docs/step-series/)
#
# Build first: tools/build_site.sh preview|production. rsync --delete removes, in that one directory, the files
# that are not in the build. .htaccess files are never sent or deleted by this script (see
# claude_docs/REPORT_r8_2_deploy_prep.md, appendix A, for how to put them). The parent directory (docs/ or
# docs-preview/) must exist on the server: this script does not create it.
set -eu
root=$(cd "$(dirname "$0")/.." && pwd)
cd "$root"

usage() { echo "usage: tools/deploy.sh preview|production [--apply]" >&2; exit 2; }
[ $# -ge 1 ] && [ $# -le 2 ] || usage
target=$1
mode=--dry-run
if [ $# -eq 2 ]; then
    case "$2" in
        --apply) mode=--apply ;;
        --dry-run) mode=--dry-run ;;
        *) usage ;;
    esac
fi

# The only two destinations. Nothing else is accepted, and nothing is built from user input.
case "$target" in
    preview)
        site_dir=site-preview
        remote_dir=docs-preview/step-series/
        url=https://ponoor.com/docs-preview/step-series/
        ;;
    production)
        site_dir=site
        remote_dir=docs/step-series/
        url=https://ponoor.com/docs/step-series/
        ;;
    *) usage ;;
esac

# Guards for --delete: the destination is exactly one of the two, with a trailing slash; the source is a
# non-empty build of the right kind.
case "$remote_dir" in
    docs-preview/step-series/ | docs/step-series/) ;;
    *) echo "deploy: refusing to use the destination '$remote_dir'" >&2; exit 1 ;;
esac
[ -f "$site_dir/index.html" ] && [ -f "$site_dir/en/index.html" ] && [ -d "$site_dir/assets" ] || {
    echo "deploy: $site_dir/ is missing or incomplete. Run: tools/build_site.sh $target" >&2; exit 1; }
n=$(find "$site_dir" -type f | wc -l | tr -d ' ')
[ "$n" -ge 100 ] || { echo "deploy: $site_dir/ has only $n files; refusing to --delete against it" >&2; exit 1; }
grep -q "<link rel=\"canonical\" href=\"$url\">" "$site_dir/index.html" || {
    echo "deploy: $site_dir/ was not built for $url. Run: tools/build_site.sh $target" >&2; exit 1; }
if [ "$target" = production ] && grep -q 'name="robots" content="noindex"' "$site_dir/index.html"; then
    echo "deploy: the production build has noindex" >&2; exit 1
fi
if [ "$target" = preview ] && ! grep -q 'name="robots" content="noindex"' "$site_dir/index.html"; then
    echo "deploy: the preview build has no noindex" >&2; exit 1
fi

dest="lolipop:web/ponoor.com/$remote_dir"
if [ "$mode" = --apply ]; then
    echo "deploy: UPLOADING $site_dir/ -> $dest ($n files; --delete in that directory only; .htaccess is left alone)"
    rsync -av --delete --exclude=.htaccess -e ssh "$site_dir/" "$dest"
else
    echo "deploy: DRY RUN (nothing is written): $site_dir/ -> $dest ($n files). Add --apply to upload."
    rsync -av --dry-run --delete --exclude=.htaccess -e ssh "$site_dir/" "$dest"
fi
