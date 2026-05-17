#!/usr/bin/env bash
#
# Create a Heimdallur GitHub release.
#
# By default this reads the project version from pyproject.toml, creates an
# annotated vX.Y.Z tag at HEAD, pushes it, and publishes a GitHub release using
# GitHub's generated release notes.
#
# Usage:
#   scripts/create-release.sh
#   scripts/create-release.sh 0.6.0
#   DRY_RUN=1 scripts/create-release.sh

set -euo pipefail

REMOTE="${REMOTE:-origin}"
TARGET="${TARGET:-HEAD}"
DRY_RUN="${DRY_RUN:-0}"
ALLOW_DIRTY="${ALLOW_DIRTY:-0}"
PRERELEASE="${PRERELEASE:-0}"
TITLE="${TITLE:-}"
NOTES_FILE="${NOTES_FILE:-}"

usage() {
  cat <<'EOF'
Usage:
  scripts/create-release.sh [VERSION]

Creates a GitHub release for Heimdallur.

Arguments:
  VERSION       Optional version, with or without a leading "v".
                If omitted, the version is read from pyproject.toml.

Environment:
  REMOTE=name       Git remote to push the tag to. Defaults to "origin".
  TARGET=ref        Commit/ref to tag. Defaults to "HEAD".
  DRY_RUN=1         Print actions without creating tags, pushing, or publishing.
  ALLOW_DIRTY=1     Allow releasing with local tracked changes.
  TITLE=text        Override the GitHub release title. Defaults to the tag.
  NOTES_FILE=path   Use explicit release notes instead of generated notes.
  PRERELEASE=1      Mark the GitHub release as a prerelease.

Prerequisites:
  - Run from the repository root.
  - gh CLI must be installed and authenticated with release permissions.
EOF
}

run() {
  if [[ "$DRY_RUN" == "1" ]]; then
    printf 'DRY RUN:'
    printf ' %q' "$@"
    printf '\n'
  else
    "$@"
  fi
}

die() {
  echo "ERROR: $*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || die "Required command not found: $1"
}

repo_root() {
  git rev-parse --show-toplevel
}

ensure_repo_root() {
  local root
  root="$(repo_root)"
  [[ "$PWD" == "$root" ]] || die "Run this script from the repository root: $root"
}

ensure_clean_worktree() {
  [[ "$DRY_RUN" == "1" ]] && return
  [[ "$ALLOW_DIRTY" == "1" ]] && return
  git diff --quiet || die "Tracked working tree changes found. Commit or stash them, or set ALLOW_DIRTY=1."
  git diff --cached --quiet || die "Staged changes found. Commit or unstage them, or set ALLOW_DIRTY=1."
}

version_from_pyproject() {
  awk -F'"' '/^version = / { print $2; exit }' pyproject.toml
}

normalize_tag() {
  local version="$1"
  [[ "$version" == v* ]] && echo "$version" || echo "v${version}"
}

ensure_ref_exists() {
  local ref="$1"
  git cat-file -e "${ref}^{commit}" 2>/dev/null || die "Target is not a commit: $ref"
}

ensure_tag() {
  local tag="$1"
  local target_commit="$2"

  if git rev-parse -q --verify "refs/tags/${tag}" >/dev/null; then
    local current
    current="$(git rev-list -n 1 "$tag")"
    [[ "$current" == "$target_commit" ]] || \
      die "Local tag $tag points at $current, expected $target_commit."
    echo "  $tag already exists locally"
    return
  fi

  echo "  creating local tag $tag at $target_commit"
  run git tag -a "$tag" "$target_commit" -m "Heimdallur ${tag}"
}

push_tag() {
  local tag="$1"

  if [[ "$DRY_RUN" == "1" ]]; then
    echo "  would push $tag to $REMOTE"
    run git push "$REMOTE" "$tag"
    return
  fi

  if git ls-remote --exit-code --tags "$REMOTE" "refs/tags/${tag}" >/dev/null 2>&1; then
    echo "  $tag already exists on $REMOTE"
    return
  fi

  echo "  pushing $tag to $REMOTE"
  run git push "$REMOTE" "$tag"
}

release_exists() {
  local tag="$1"
  [[ "$DRY_RUN" == "1" ]] && return 1
  gh release view "$tag" >/dev/null 2>&1
}

create_release() {
  local tag="$1"
  local title="$2"
  local args=("$tag" "--title" "$title")

  if [[ -n "$NOTES_FILE" ]]; then
    [[ -f "$NOTES_FILE" ]] || die "NOTES_FILE does not exist: $NOTES_FILE"
    args+=("--notes-file" "$NOTES_FILE")
  else
    args+=("--generate-notes")
  fi

  if [[ "$PRERELEASE" == "1" ]]; then
    args+=("--prerelease")
  fi

  if release_exists "$tag"; then
    echo "  GitHub release $tag already exists"
    return
  fi

  echo "  creating GitHub release $tag"
  run gh release create "${args[@]}"
}

main() {
  if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
    exit 0
  fi

  require_command git
  require_command gh
  ensure_repo_root
  ensure_clean_worktree

  if [[ "$DRY_RUN" != "1" ]]; then
    gh auth status >/dev/null || die "gh is not authenticated. Run: gh auth login"
  fi

  local version tag target_commit title
  version="${1:-$(version_from_pyproject)}"
  [[ -n "$version" ]] || die "Could not determine version. Pass VERSION or set pyproject.toml [project].version."

  tag="$(normalize_tag "$version")"
  title="${TITLE:-$tag}"

  ensure_ref_exists "$TARGET"
  target_commit="$(git rev-parse "$TARGET^{commit}")"

  echo "==> Release plan"
  echo "  tag:    $tag"
  echo "  target: $target_commit"
  echo "  remote: $REMOTE"
  [[ "$DRY_RUN" == "1" ]] && echo "  mode:   dry run"

  echo "==> Creating tag"
  ensure_tag "$tag" "$target_commit"

  echo "==> Pushing tag"
  push_tag "$tag"

  echo "==> Creating GitHub release"
  create_release "$tag" "$title"

  echo ""
  echo "All done: https://github.com/arnthorsnaer/HeimDallur/releases/tag/${tag}"
}

main "$@"
