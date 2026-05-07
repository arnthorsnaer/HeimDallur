import argparse
import asyncio


def main() -> None:
    parser = argparse.ArgumentParser(description="Heimdallur network monitor")
    parser.add_argument(
        "--mode",
        choices=["tui", "status", "report"],
        default="tui",
        help=(
            "tui: interactive dashboard (default)  |  "
            "status: single-pass rich output  |  "
            "report: write markdown snapshot to ~/.local/share/heimdallur/status.md and print it"
        ),
    )
    args = parser.parse_args()

    if args.mode == "tui":
        from heimdallur.tui.app import HeimdallurApp
        HeimdallurApp().run()
    elif args.mode == "status":
        from heimdallur.status.render import render_status
        asyncio.run(render_status())
    else:
        from heimdallur.core.report import run_report
        content = asyncio.run(run_report())
        print(content)


if __name__ == "__main__":
    main()
