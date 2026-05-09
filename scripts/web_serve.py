#!/usr/bin/env python3
"""Start Heimdallur as a browser-accessible web UI via textual-serve.

Usage:
    python scripts/web_serve.py [--host HOST] [--port PORT]

Serves the TUI at http://<host>:<port>/ using xterm.js in the browser.
Environment variables (NETWATCH_MOCK, NETWATCH_MOCK_SCENARIO, etc.) are
forwarded to the app subprocess automatically.
"""
from __future__ import annotations

import argparse
from textual_serve.server import Server


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    server = Server(
        "python -m heimdallur --mode tui",
        host=args.host,
        port=args.port,
        title="Heimdallur",
    )
    print(f"Serving Heimdallur at http://{args.host}:{args.port}/")
    print("Press Ctrl+C to stop.")
    server.serve()


if __name__ == "__main__":
    main()
