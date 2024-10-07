import os

from playwright.sync_api import Page


def handle_perform_logout_redirection_to_login(page: Page, screenshots_dir: str):
    page.wait_for_url('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login', timeout=30000)
    # page.wait_for_url('https://opensource-demo.orangehrmlive.com/auth/login', timeout=30000)
    try:
        page.screenshot(path=os.path.join(screenshots_dir, "after_logout.png"))
    except TimeoutError:
        print("Timeout waiting for redirect to the login page.")
        print("Current URL:", page.url)
        # Take screenshot in case of error
        page.screenshot(path=os.path.join(screenshots_dir, "error.png"))


"""
def handle_perform_logout_redirection_to_login(page: Page, screenshots_dir: str):
    login_url = 'https://opensource-demo.orangehrmlive.com/auth/login'
    try:
        page.wait_for_url(login_url, timeout=30000)
    except TimeoutError:
        print("Timeout waiting for redirect to the login page.")
        print(f"Current URL: {page.url}")
        capture_screenshot(page, screenshots_dir, "error.png")
"""
