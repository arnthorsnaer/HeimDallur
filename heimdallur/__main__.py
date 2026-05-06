import argparse
import asyncio


def main() -> None:
    parser = argparse.ArgumentParser(description="Heimdallur network monitor")
    parser.add_argument(
        "--mode",
        choices=["tui", "status"],
        default="tui",
        help="tui: interactive dashboard (default)  |  status: single-pass rich output",
    )
    args = parser.parse_args()

    if args.mode == "tui":
        from heimdallur.tui.app import HeimdallurApp
        HeimdallurApp().run()
    else:
        from heimdallur.status.render import render_status
        asyncio.run(render_status())


if __name__ == "__main__":
    main()
