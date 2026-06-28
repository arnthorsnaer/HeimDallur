#!/usr/bin/env python3
"""Start Heimdallur as a browser-accessible web UI via textual-serve.

Usage:
    python scripts/web_serve.py [--host HOST] [--port PORT]

Serves the TUI at http://<host>:<port>/ using xterm.js in the browser.
By default this binds to localhost and starts Heimdallur in shared-state viewer
mode, so the web UI reuses the tty app's latest probe results instead of
running a second prober. Pass --host explicitly when exposing the service beyond
the local machine, ideally behind network controls or a reverse proxy with auth.
Use --standalone to run a full probing app in the browser process.
Environment variables (HEIMDALLUR_CONFIG, HEIMDALLUR_STATE_FILE, etc.) are
forwarded to the app subprocess automatically.
"""
from __future__ import annotations

import argparse
import os
import time
from pathlib import Path

from aiohttp import web
from textual_serve.server import Server


_DEFAULT_STATUS_PATH = Path.home() / ".local" / "share" / "heimdallur" / "status.md"


def _status_path() -> Path:
    return Path(os.getenv("HEIMDALLUR_STATUS_FILE", str(_DEFAULT_STATUS_PATH))).expanduser()


class HeimdallurWebServer(Server):
    async def _make_app(self) -> web.Application:
        app = await super()._make_app()
        app.router.add_get("/status.md", self.handle_status_md)
        return app

    async def handle_status_md(self, request: web.Request) -> web.Response:
        path = _status_path()
        try:
            content = path.read_text()
            mtime = path.stat().st_mtime
        except FileNotFoundError:
            return web.Response(
                status=404,
                text="Heimdallur status.md has not been written yet.\n",
                content_type="text/plain",
            )
        except OSError as exc:
            return web.Response(
                status=503,
                text=f"Unable to read Heimdallur status.md: {exc}\n",
                content_type="text/plain",
            )

        age = max(0, int(time.time() - mtime))
        return web.Response(
            text=content,
            content_type="text/markdown",
            headers={
                "Cache-Control": "no-store",
                "X-Heimdallur-Status-Age-Seconds": str(age),
            },
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument(
        "--standalone",
        action="store_true",
        help="run a full probing app instead of the shared-state viewer",
    )
    args = parser.parse_args()

    command = "python -m heimdallur --mode tui" if args.standalone else "python -m heimdallur --mode view"
    server = HeimdallurWebServer(
        command,
        host=args.host,
        port=args.port,
        title="Heimdallur",
    )
    print(f"Serving Heimdallur at http://{args.host}:{args.port}/")
    print(f"Serving status markdown at http://{args.host}:{args.port}/status.md")
    print("Press Ctrl+C to stop.")
    server.serve()


if __name__ == "__main__":
    main()
