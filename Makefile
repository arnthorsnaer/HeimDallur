.PHONY: mock dev status-render web install clean deploy logs pi-status

# Development — live reload on Python/TOML changes via watchfiles
dev:
	NETWATCH_MOCK=1 uv run watchfiles "python -m heimdallur --mode tui" heimdallur/

# Simple one-shot run in mock mode (no reload)
mock:
	NETWATCH_MOCK=1 uv run python -m heimdallur --mode tui

# Single-pass rich status render (no TUI)
status-render:
	NETWATCH_MOCK=1 uv run python -m heimdallur --mode status

# Serve the TUI in a browser via xterm.js (http://localhost:8080)
web:
	uv run python scripts/web_serve.py

# Mock mode web server (no real pings)
web-mock:
	NETWATCH_MOCK=1 uv run python scripts/web_serve.py

install:
	uv sync

# ── Pi deployment ──────────────────────────────────────────────
deploy:
	@echo "==> Syncing to Pi..."
	rsync -avz --exclude '.git' --exclude '__pycache__' --exclude '.venv' \
		. pi@heimdallur.local:/opt/heimdallur/
	ssh pi@heimdallur.local "cd /opt/heimdallur && uv sync --no-dev && sudo systemctl restart heimdallur"
	@echo "==> Done."

logs:
	ssh pi@heimdallur.local "journalctl -u heimdallur -f"

pi-status:
	ssh pi@heimdallur.local "systemctl status heimdallur"

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
