"""

This project implements an automated testing framework for login and logout functionalities using Playwright and
Python, designed to validate the login capabilities of a web application by utilizing configuration data stored in a
dedicated config file. The framework is built using a modular design, encapsulating specific functionalities such as
navigation to the login page, handling login actions with user credentials, performing logout operations,
and managing browser sessions. It employs the Page Object Model (POM) design pattern, where each page of the
application corresponds to a dedicated class, enhancing maintainability and readability. Configuration management is
achieved through a centralized config file, making it easy to update user credentials and the base URL without
altering the core test logic. Additionally, the framework captures screenshots at critical points—before and after
login attempts, post-logout, and in cases of errors—facilitating visual validation and debugging. Robust error
handling is also implemented, logging any issues during test execution and capturing relevant screenshots to aid in
troubleshooting.

"""
# pytest tests\test_login_with_config_data.py
import sys
import os

# Add the parent directory to the Python path before importing any modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from the modules folder
import json
import pytest

from playwright.sync_api import sync_playwright, Page
from config.config import Config
from modules.navigate_to_login_page import handle_navigate_to_login_page
from modules.perform_login_with_config_data import handle_perform_login_with_config_data
from modules.perform_logout import handle_perform_logout
from modules.perform_logout_redirection_to_login import handle_perform_logout_redirection_to_login
from modules.close_browser import handle_close_browser


def setup_browser(headless=False):
    """Initialize Playwright, launch the browser, and open a new page."""
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    page = browser.new_page()
    return playwright, browser, page


def setup_screenshot_directory():
    """Set up the directory to store screenshots."""
    screenshots_dir = 'screenshots'
    os.makedirs(screenshots_dir, exist_ok=True)
    return screenshots_dir


def capture_screenshot(page, screenshots_dir, filename):
    """Capture a screenshot and save it to the specified directory."""
    os.makedirs(screenshots_dir, exist_ok=True)
    page.screenshot(path=os.path.join(screenshots_dir, filename))


def navigate_to_login_page(page: Page):
    handle_navigate_to_login_page(page)


def perform_login_with_jason_data(page: Page):
    handle_perform_login_with_config_data(page)


def perform_logout(page: Page):
    handle_perform_logout(page)


def perform_logout_redirection_to_login(page: Page, screenshots_dir: str):
    handle_perform_logout_redirection_to_login(page, screenshots_dir)


def close_browser(playwright, browser):
    handle_close_browser(playwright, browser)


def perform_test(page: Page, screenshots_dir: str):
    """Perform the login, capture screenshots, and perform logout for all users."""

    # Loop through all users in the Config
    for user in Config.USERS:
        username = user['username']
        password = user['password']

        # Navigate to login page and wait for it to load
        navigate_to_login_page(page)
        page.screenshot(path=os.path.join(screenshots_dir, f"before_login_{username}.png"))

        try:
            # Perform login with the loaded credentials
            handle_perform_login_with_config_data(page, username, password)
            page.screenshot(path=os.path.join(screenshots_dir, f"after_login_{username}.png"))

            # Check if the login was successful
            if page.url == 'https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index':
                # Perform logout and capture a screenshot
                perform_logout(page)
                page.wait_for_url(Config.BASE_URL, timeout=30000)
                page.screenshot(path=os.path.join(screenshots_dir, f"after_logout_{username}.png"))
            else:
                # Handle login failure (e.g., stay on the login page or show an error)
                print(f"Login failed for user {username}. Staying on login page.")
                page.screenshot(path=os.path.join(screenshots_dir, f"login_failed_{username}.png"))

        except Exception as e:
            print(f"Error during login/logout tests for user {username}: {str(e)}")
            page.screenshot(path=os.path.join(screenshots_dir, f"error_{username}.png"))
            raise


def test_login_with_config_data():
    """Main test function to perform login and logout using config data."""
    playwright, browser, page = setup_browser()  # This will default to headless=False
    screenshots_dir = setup_screenshot_directory()

    try:
        perform_test(page, screenshots_dir)
    except Exception as e:
        print(f"Error during login/logout tests: {str(e)}")
        page.screenshot(path=os.path.join(screenshots_dir, "error.png"))
        raise
    finally:
        close_browser(playwright, browser)


# Entry point for running the tests directly
if __name__ == "__main__":
    test_login_with_config_data()
