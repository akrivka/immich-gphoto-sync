import asyncio
import argparse
import os
from pathlib import Path

from playwright.async_api import async_playwright

from config import USER_DATA_FOLDER


async def main() -> None:
    parser = argparse.ArgumentParser(description='Authenticate with Google Photos')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode with remote debugging')
    parser.add_argument('--remote-debugging-port', type=int, default=9222, help='Port for remote debugging')
    args = parser.parse_args()

    async with async_playwright() as p:
        browser_args = [
            "--disable-blink-features=AutomationControlled",
        ]
        
        if args.headless:
            browser_args.extend([
                f"--remote-debugging-port={args.remote_debugging_port}",
                "--remote-debugging-address=0.0.0.0"
            ])
            print(f"Running in headless mode with remote debugging on port {args.remote_debugging_port}")
            print(f"Connect to http://SERVER_IP:{args.remote_debugging_port} from another computer with Chrome")
            print(f"User data will be saved to: {USER_DATA_FOLDER}")
        
        browser = await p.chromium.launch_persistent_context(
            USER_DATA_FOLDER,
            headless=args.headless,
            args=browser_args,
        )
        page = await browser.new_page()
        await page.goto("https://photos.google.com/")
        
        if args.headless:
            print("Waiting for authentication. Press Ctrl+C when done.")
            # Keep the browser open for remote access
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                print("Authentication process stopped. Check if user data was saved.")
        else:
            # Original behavior - wait for the browser window to be closed
            await page.wait_for_event("close", timeout=0)


if __name__ == "__main__":
    asyncio.run(main())