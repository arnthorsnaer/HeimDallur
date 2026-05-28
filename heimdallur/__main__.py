import argparse
import asyncio
from pathlib import Path

from heimdallur.config.loader import resolve_config_path
from heimdallur.config.validator import format_validation_result, validate_config


def main() -> None:
    parser = argparse.ArgumentParser(description="Heimdallur network monitor")
    parser.add_argument(
        "--mode",
        choices=["tui", "view", "status", "report", "validate-config"],
        default="tui",
        help=(
            "tui: interactive dashboard + probe loop (default)  |  "
            "view: dashboard fed from shared live state, no probes  |  "
            "status: single-pass rich output  |  "
            "report: write markdown snapshot to ~/.local/share/heimdallur/status.md and print it  |  "
            "validate-config: validate network TOML and exit"
        ),
    )
    parser.add_argument(
        "config_path",
        nargs="?",
        help="optional TOML path for --mode validate-config",
    )
    args = parser.parse_args()

    if args.mode == "validate-config":
        path = resolve_config_path(Path(args.config_path).expanduser() if args.config_path else None)
        result = validate_config(path)
        print(format_validation_result(result))
        raise SystemExit(0 if result.ok else 1)

    path = resolve_config_path()
    result = validate_config(path)
    if not result.ok:
        print(format_validation_result(result))
        if args.mode in ("tui", "view"):
            from heimdallur.tui.error_view import ConfigErrorApp
            ConfigErrorApp(result).run()
            return
        raise SystemExit(1)

    if args.mode in ("tui", "view"):
        from heimdallur.tui.app import HeimdallurApp
        HeimdallurApp(viewer=args.mode == "view").run()
    elif args.mode == "status":
        from heimdallur.status.render import render_status
        asyncio.run(render_status())
    else:
        from heimdallur.core.report import run_report
        content = asyncio.run(run_report())
        print(content)


if __name__ == "__main__":
    main()
