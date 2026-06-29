#!/usr/bin/env bash
# Auto-update Heimdallur from the configured update channel.
# Designed to be run by a systemd timer (see scripts/heimdallur-update.timer).
# Exits 0 whether or not an update was applied.

set -euo pipefail

APP_DIR="${APP_DIR:-/opt/heimdallur}"
SERVICE="${SERVICE:-heimdallur}"
REMOTE="${REMOTE:-origin}"
BRANCH="${BRANCH:-main}"
TAG_PATTERN="${TAG_PATTERN:-v[0-9]*}"
TARGET_TAG="${TARGET_TAG:-}"
UPDATE_CONFIG="${UPDATE_CONFIG:-${HEIMDALLUR_CONFIG:-}}"
LOG_TAG="heimdallur-update"

log() { logger -t "$LOG_TAG" "$*"; echo "$(date -Iseconds) $*"; }
die() { log "ERROR: $*"; exit 1; }

latest_release_tag() {
    git tag --list "$TAG_PATTERN" --sort=-version:refname | head -1
}

config_path() {
    if [[ -n "$UPDATE_CONFIG" ]]; then
        echo "$UPDATE_CONFIG"
    else
        echo "$HOME/.config/heimdallur/network.toml"
    fi
}

update_channel() {
    if [[ -n "${UPDATE_CHANNEL:-}" ]]; then
        echo "$UPDATE_CHANNEL"
        return
    fi

    local cfg
    cfg="$(config_path)"
    if [[ ! -f "$cfg" ]]; then
        echo "release"
        return
    fi

    awk '
        /^\[updates\][[:space:]]*$/ { in_updates=1; next }
        /^\[/ { in_updates=0 }
        in_updates && /^[[:space:]]*channel[[:space:]]*=/ {
            value=$0
            sub(/^[^=]*=[[:space:]]*/, "", value)
            sub(/[[:space:]]*(#.*)?$/, "", value)
            gsub(/^"|"$/, "", value)
            print value
            found=1
            exit
        }
        END { if (!found) print "release" }
    ' "$cfg"
}

version_from_pyproject() {
    awk -F'"' '/^version = / { print $2; exit }' pyproject.toml
}

require_clean_checkout() {
    if [[ -n "$(git status --short)" ]]; then
        die "Working tree is dirty; refusing to update. Run: cd $APP_DIR && git status --short"
    fi
}

sync_and_restart() {
    uv sync --no-dev --frozen --quiet
    log "Dependencies synced."

    systemctl restart "$SERVICE"
    log "Service restarted. Update complete."
}

update_release() {
    log "Checking for tagged release updates..."
    git fetch "$REMOTE" --tags --prune --quiet

    if [[ -z "$TARGET_TAG" ]]; then
        TARGET_TAG="$(latest_release_tag)"
    fi
    [[ -n "$TARGET_TAG" ]] || die "No release tags matching $TAG_PATTERN found."

    git rev-parse -q --verify "refs/tags/$TARGET_TAG" >/dev/null || die "Target tag not found: $TARGET_TAG"

    local local_commit target_commit current_tag expected_version project_version
    local_commit="$(git rev-parse HEAD)"
    target_commit="$(git rev-list -n 1 "$TARGET_TAG")"
    current_tag="$(git describe --tags --exact-match HEAD 2>/dev/null || true)"
    expected_version="${TARGET_TAG#v}"

    if [[ "$local_commit" == "$target_commit" ]]; then
        log "Already on $TARGET_TAG ($local_commit)."
        exit 0
    fi

    log "Update available: ${current_tag:-$local_commit} -> $TARGET_TAG ($target_commit)"

    git checkout --detach "$TARGET_TAG" --quiet
    log "Checked out $TARGET_TAG."

    project_version="$(version_from_pyproject)"
    if [[ "$project_version" != "$expected_version" ]]; then
        die "Version mismatch after checkout: pyproject.toml has $project_version, expected $expected_version from $TARGET_TAG"
    fi
    log "Verified release version $project_version."

    sync_and_restart
}

update_edge() {
    log "Checking for edge updates from $REMOTE/$BRANCH..."
    git fetch "$REMOTE" "$BRANCH" --quiet

    local local_commit target_commit
    local_commit="$(git rev-parse HEAD)"
    target_commit="$(git rev-parse "$REMOTE/$BRANCH")"

    if [[ "$local_commit" == "$target_commit" ]]; then
        log "Already on $REMOTE/$BRANCH ($local_commit)."
        exit 0
    fi

    log "Edge update available: $local_commit -> $target_commit"
    if git show-ref --verify --quiet "refs/heads/$BRANCH"; then
        git checkout "$BRANCH" --quiet
        git merge --ff-only "$REMOTE/$BRANCH" --quiet
    else
        git checkout -B "$BRANCH" "$REMOTE/$BRANCH" --quiet
    fi
    log "Checked out $REMOTE/$BRANCH."

    sync_and_restart
}

cd "$APP_DIR"
require_clean_checkout

CHANNEL="$(update_channel)"
log "Update channel: $CHANNEL"

case "$CHANNEL" in
    off)
        log "Auto-update disabled by config."
        exit 0
        ;;
    release)
        update_release
        ;;
    edge)
        update_edge
        ;;
    *)
        die "Invalid update channel '$CHANNEL' in $(config_path). Expected one of: off, release, edge."
        ;;
esac
