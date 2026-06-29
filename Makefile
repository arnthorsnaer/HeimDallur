.PHONY: mock dev status-render web install clean deploy logs pi-status pi-update pi-sync-config pi-web-status

# Development — live reload on Python/TOML changes via watchfiles
dev:
	HEIMDALLUR_MOCK=1 uv run watchfiles "python -m heimdallur --mode tui" heimdallur/

# Simple one-shot run in mock mode (no reload)
mock:
	HEIMDALLUR_MOCK=1 uv run python -m heimdallur --mode tui

# Single-pass rich status render (no TUI)
status-render:
	HEIMDALLUR_MOCK=1 uv run python -m heimdallur --mode status

# Serve the TUI in a browser via xterm.js (http://localhost:8080)
web:
	uv run python scripts/web_serve.py

# Mock mode web server (no real pings)
web-mock:
	HEIMDALLUR_MOCK=1 uv run python scripts/web_serve.py

install:
	uv sync

# ── Configurable Pi maintenance ─────────────────────────────────
# Override these from the environment or command line, for example:
#   make pi-status PI_USER=arnthorsnaer PI_HOST=heimdallur.local
PI_HOST ?= heimdallur.local
PI_USER ?= pi
PI_SSH ?= $(PI_USER)@$(PI_HOST)
PI_APP_DIR ?= /opt/heimdallur
PI_UV ?= uv
PI_UPDATE_SERVICE ?= heimdallur-update.service
PI_CONFIG_SRC ?= $(HOME)/.config/heimdallur/network.toml
PI_CONFIG_DEST ?= ~/.config/heimdallur/network.toml
PI_RESTART_DISPLAY ?= sudo systemctl restart heimdallur
PI_RESTART_WEB ?=

# Backwards-compatible code sync helper for maintainer/dev workflows.
deploy:
	@echo "==> Syncing code to $(PI_SSH):$(PI_APP_DIR)..."
	rsync -avz --exclude '.git' --exclude '__pycache__' --exclude '.venv' \
		. $(PI_SSH):$(PI_APP_DIR)/
	ssh $(PI_SSH) "cd $(PI_APP_DIR) && $(PI_UV) sync --no-dev"
	$(if $(strip $(PI_RESTART_DISPLAY)),ssh $(PI_SSH) "$(PI_RESTART_DISPLAY)")
	$(if $(strip $(PI_RESTART_WEB)),ssh $(PI_SSH) "$(PI_RESTART_WEB)")
	@echo "==> Done."

logs:
	ssh $(PI_SSH) "journalctl -u heimdallur -f"

pi-update:
	ssh $(PI_SSH) "sudo systemctl start $(PI_UPDATE_SERVICE)"

pi-sync-config:
	@echo "==> Syncing config $(PI_CONFIG_SRC) -> $(PI_SSH):$(PI_CONFIG_DEST)"
	ssh $(PI_SSH) "mkdir -p \$$(dirname $(PI_CONFIG_DEST))"
	rsync -avz $(PI_CONFIG_SRC) $(PI_SSH):$(PI_CONFIG_DEST)
	ssh $(PI_SSH) "chmod 600 $(PI_CONFIG_DEST)"
	$(if $(strip $(PI_RESTART_DISPLAY)),ssh $(PI_SSH) "$(PI_RESTART_DISPLAY)")
	$(if $(strip $(PI_RESTART_WEB)),ssh $(PI_SSH) "$(PI_RESTART_WEB)")

pi-status:
	ssh $(PI_SSH) "set -e; cd $(PI_APP_DIR); printf 'commit: '; git log -1 --oneline; printf 'version: '; $(PI_UV) run python -c 'from heimdallur.version import __version__; print(__version__)'; $(PI_UV) run python scripts/pi-doctor.py --app-dir $(PI_APP_DIR)"

pi-web-status:
	ssh $(PI_SSH) 'systemctl status heimdallur-web.service --no-pager -l || true; ss -tulpn | grep -E ":(80|8080) " || true'

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
