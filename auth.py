import asyncio
import argparse
import os
import socket
from pathlib import Path

from playwright.async_api import async_playwright

from config import USER_DATA_FOLDER


def get_local_ip():
    """Get the local IP address of the machine."""
    try:
        # Create a temporary socket to determine the local IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Doesn't actually send any data
            s.connect(('8.8.8.8', 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        return '0.0.0.0'


async def main() -> None:
    parser = argparse.ArgumentParser(description='Authenticate with Google Photos')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode with remote debugging')
    parser.add_argument('--remote-debugging-port', type=int, default=9222, help='Port for remote debugging')
    args = parser.parse_args()

    # Get the local IP address
    local_ip = get_local_ip()

    async with async_playwright() as p:
        # More comprehensive browser arguments
        browser_args = [
            "--disable-blink-features=AutomationControlled",
            f"--remote-debugging-port={args.remote_debugging_port}",
            f"--remote-debugging-address={local_ip}",  # Use detected local IP
        ]
        
        if args.headless:
            browser_args.extend([
                "--headless",  # Explicitly add headless flag
                "--remote-debugging-bind-address=0.0.0.0"
            ])
            print(f"Running in headless mode with remote debugging")
            print(f"Remote debugging IP: {local_ip}")
            print(f"Remote debugging port: {args.remote_debugging_port}")
            print(f"User data will be saved to: {USER_DATA_FOLDER}")
        
        print("Final browser args:", browser_args)
        
        try:
            # Use launch instead of launch_persistent_context for more control
            browser = await p.chromium.launch(
                headless=args.headless,
                args=browser_args,
                user_data_dir=USER_DATA_FOLDER
            )
            
            # Create a context
            context = await browser.new_context()
            page = await context.new_page()
            
            await page.goto("https://photos.google.com/")
            
            if args.headless:
                print("Waiting for authentication. Press Ctrl+C when done.")
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    print("Authentication process stopped. Check if user data was saved.")
            else:
                # Original behavior - wait for the browser window to be closed
                await page.wait_for_event("close", timeout=0)
        
        except Exception as e:
            print(f"Error during browser launch: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())