#!/usr/bin/env bash
# Auto-update Heimdallur from the public GitHub repo.
# Designed to be run by a systemd timer (see scripts/heimdallur-update.timer).
# Exits 0 whether or not an update was applied.

set -euo pipefail

APP_DIR="/opt/heimdallur"
SERVICE="heimdallur"
BRANCH="main"
LOG_TAG="heimdallur-update"

log() { logger -t "$LOG_TAG" "$*"; echo "$(date -Iseconds) $*"; }

cd "$APP_DIR"

log "Checking for updates..."
git fetch origin "$BRANCH" --quiet

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse "origin/$BRANCH")

if [[ "$LOCAL" == "$REMOTE" ]]; then
    log "Already up to date ($LOCAL)."
    exit 0
fi

COMMITS=$(git log --oneline "$LOCAL".."$REMOTE" | head -10)
log "Update available: $LOCAL -> $REMOTE"
log "New commits:"
while IFS= read -r line; do log "  $line"; done <<< "$COMMITS"

git pull --ff-only origin "$BRANCH"
log "Code updated."

uv sync --no-dev --quiet
log "Dependencies synced."

systemctl restart "$SERVICE"
log "Service restarted. Update complete."
