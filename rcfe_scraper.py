"""
RCFE Data Scraper
Downloads RCFE (Residential Care Facilities for the Elderly) data from CCLD website
"""

import os
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def download_rcfe_data(download_dir="./data"):
    """
    Scrapes and downloads RCFE data from the CCLD download page

    Args:
        download_dir: Directory where the downloaded file will be saved
    """
    # Create download directory if it doesn't exist
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
        print(f"Created download directory: {download_dir}")

    # Make download directory absolute path
    download_dir = os.path.abspath(download_dir)

    print("Starting RCFE data scraper...")
    print(f"Download directory: {download_dir}")

    with sync_playwright() as p:
        # Launch browser (use headless=False to see what's happening)
        print("Launching browser...")
        browser = p.chromium.launch(headless=False)  # Set to True for background execution

        # Create a new page with download settings
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        try:
            # Navigate to the main search page first
            url = "https://www.ccld.dss.ca.gov/carefacilitysearch/"
            print(f"Navigating to: {url}")
            page.goto(url, wait_until="networkidle", timeout=60000)

            # Wait for the page to fully load
            print("Waiting for main page to load...")
            try:
                page.wait_for_selector("body", timeout=30000)
                page.wait_for_timeout(3000)
                print("Main page loaded")
            except:
                print("Warning: Timeout waiting for page elements, continuing anyway...")

            # Find and click the "Download Data" link at the top
            print("Looking for 'Download Data' link...")
            try:
                download_data_link = page.get_by_text("Download Data", exact=False)
                if download_data_link.count() > 0:
                    print("Found 'Download Data' link, clicking it...")
                    download_data_link.first.click()

                    # Wait for the download page to load
                    print("Waiting for download page to load...")
                    page.wait_for_timeout(5000)
                    print("Download page loaded")
                else:
                    print("ERROR: Could not find 'Download Data' link")
                    browser.close()
                    return False
            except Exception as e:
                print(f"ERROR: Failed to click 'Download Data' link: {e}")
                browser.close()
                return False

            # Take a screenshot for debugging
            print("Taking screenshot for debugging...")
            page.screenshot(path="./data/page_screenshot.png")
            print("Screenshot saved to ./data/page_screenshot.png")

            # Look for the RCFE link
            # We'll try multiple strategies to find it
            print("Looking for RCFE download link...")
            print(f"Page title: {page.title()}")

            # Strategy 1: Look for "Elderly Assisted Living" (the exact button text)
            rcfe_link = None
            try:
                rcfe_link = page.get_by_text("Elderly Assisted Living", exact=False)
                if rcfe_link.count() > 0:
                    print("Strategy 1 success: Found RCFE link by 'Elderly Assisted Living' text")
            except Exception as e:
                print(f"Strategy 1 failed: {e}")

            # Strategy 2: Look for text containing "Residential Care Facilities for the Elderly"
            if not rcfe_link or rcfe_link.count() == 0:
                try:
                    rcfe_link = page.get_by_text("Residential Care Facilities for the Elderly", exact=False)
                    if rcfe_link.count() > 0:
                        print("Strategy 2 success: Found RCFE link by full text")
                except Exception as e:
                    print(f"Strategy 2 failed: {e}")

            # Strategy 3: Look for "RCFE" text
            if not rcfe_link or rcfe_link.count() == 0:
                try:
                    rcfe_link = page.get_by_text("RCFE", exact=False)
                    if rcfe_link.count() > 0:
                        print("Strategy 3 success: Found RCFE link by abbreviation")
                except Exception as e:
                    print(f"Strategy 3 failed: {e}")

            # Strategy 4: Look for buttons containing "Elderly"
            if not rcfe_link or rcfe_link.count() == 0:
                try:
                    rcfe_link = page.locator("button").filter(has_text="Elderly")
                    if rcfe_link.count() > 0:
                        print(f"Strategy 4 success: Found {rcfe_link.count()} button(s) containing 'Elderly'")
                except Exception as e:
                    print(f"Strategy 4 failed: {e}")

            if not rcfe_link or rcfe_link.count() == 0:
                print("ERROR: Could not find RCFE download link on the page")
                print("Page content preview:")
                print(page.content()[:1000])
                print("\n--- Trying to find all clickable elements ---")
                all_clickable = page.locator("a, button, [role='button']").all()
                print(f"Found {len(all_clickable)} clickable elements")
                for i, elem in enumerate(all_clickable[:10]):  # Print first 10
                    try:
                        text = elem.inner_text()
                        if text.strip():
                            print(f"  {i}: {text[:50]}")
                    except:
                        pass
                browser.close()
                return False

            # Click the RCFE link first
            print("Clicking RCFE download link...")
            rcfe_link.first.click()

            # Handle the confirmation dialog that appears
            print("Waiting for confirmation dialog...")
            page.wait_for_timeout(4000)  # Wait 4 seconds for dialog to appear

            # Check if the popup with the specific message appeared
            try:
                popup_text = page.locator("text=/Large datasets can take/i")
                if popup_text.count() > 0:
                    print("✓ Confirmation popup detected (found 'Large datasets can take' text)")
                else:
                    print("Warning: Expected popup text not found")
            except Exception as e:
                print(f"Note: Could not verify popup text: {e}")

            # Look for and click the confirmation button
            try:
                # Debug: Print all buttons on the page
                all_buttons = page.locator("button").all()
                print(f"Found {len(all_buttons)} total buttons on page")
                for i, btn in enumerate(all_buttons[:5]):  # Show first 5 buttons
                    try:
                        btn_text = btn.inner_text()
                        print(f"  Button {i}: '{btn_text}'")
                    except:
                        pass

                # Try multiple strategies to find the Confirm button
                confirm_button = None

                # Strategy 1: Case-insensitive text match for "Confirm"
                try:
                    confirm_button = page.locator("button", has_text="Confirm")
                    if confirm_button.count() > 0:
                        print(f"Strategy 1 success: Found {confirm_button.count()} button(s) with 'Confirm' text")
                except Exception as e:
                    print(f"Strategy 1 failed: {e}")

                # Strategy 2: Exact case-sensitive match
                if not confirm_button or confirm_button.count() == 0:
                    try:
                        confirm_button = page.get_by_role("button", name="Confirm")
                        if confirm_button.count() > 0:
                            print(f"Strategy 2 success: Found button by role")
                    except Exception as e:
                        print(f"Strategy 2 failed: {e}")

                # Strategy 3: Look for any button containing "confirm" (case-insensitive)
                if not confirm_button or confirm_button.count() == 0:
                    try:
                        all_btns = page.locator("button").all()
                        for btn in all_btns:
                            text = btn.inner_text().lower()
                            if "confirm" in text:
                                confirm_button = btn
                                print(f"Strategy 3 success: Found button with text '{btn.inner_text()}'")
                                break
                    except Exception as e:
                        print(f"Strategy 3 failed: {e}")

                if confirm_button and (isinstance(confirm_button, object)):
                    print("Clicking Confirm button...")

                    # Set up download handler BEFORE clicking the confirmation button
                    with page.expect_download(timeout=60000) as download_info:
                        if hasattr(confirm_button, 'click'):
                            confirm_button.click()
                        else:
                            confirm_button.first.click()
                        print("Waiting for download to start...")

                    # Wait for download to complete
                    print("Download started, waiting for completion...")
                    download = download_info.value
                else:
                    print("ERROR: Could not find Confirm button")
                    browser.close()
                    return False

            except Exception as e:
                print(f"Error handling confirmation dialog: {e}")
                browser.close()
                return False

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"rcfe_data_{timestamp}.csv"
            filepath = os.path.join(download_dir, filename)

            # Save the download
            download.save_as(filepath)
            print(f"✓ Download successful!")
            print(f"✓ File saved to: {filepath}")

            # Also save a copy as "latest" for easy access
            latest_filepath = os.path.join(download_dir, "rcfe_data_latest.csv")
            download.save_as(latest_filepath)
            print(f"✓ Latest copy saved to: {latest_filepath}")

            browser.close()
            return True

        except PlaywrightTimeoutError as e:
            print(f"ERROR: Timeout while loading page or waiting for elements")
            print(f"Details: {e}")
            browser.close()
            return False

        except Exception as e:
            print(f"ERROR: An error occurred during scraping")
            print(f"Details: {e}")
            browser.close()
            return False


if __name__ == "__main__":
    print("=" * 60)
    print("RCFE Data Scraper")
    print("=" * 60)

    success = download_rcfe_data()

    if success:
        print("\n" + "=" * 60)
        print("SUCCESS: RCFE data downloaded successfully!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("FAILED: Could not download RCFE data")
        print("Please check the error messages above")
        print("=" * 60)
