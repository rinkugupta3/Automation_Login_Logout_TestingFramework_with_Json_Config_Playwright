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
# pytest tests\test_login_with_json_data.py

import sys
import os

# Add the parent directory to the Python path before importing any modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you can import from the modules folder
import json
import pytest
from playwright.sync_api import sync_playwright, Page

from modules.navigate_to_login_page import handle_navigate_to_login_page
from modules.perform_login_with_json_data import handle_perform_login_with_json_data
from modules.perform_logout import handle_perform_logout
from modules.perform_logout_redirection_to_login import handle_perform_logout_redirection_to_login
from modules.close_browser import handle_close_browser


def load_login_data():
    """Load login data from a JSON file."""
    json_file_path = os.path.join('test_data', 'json_login_data.json')

    with open(json_file_path) as json_file:
        data = json.load(json_file)

    return data


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


def perform_login_with_jason_data(page: Page, username: str, password: str):
    handle_perform_login_with_json_data(page, username, password)


def perform_logout(page: Page):
    handle_perform_logout(page)


def perform_logout_redirection_to_login(page: Page, screenshots_dir: str):
    handle_perform_logout_redirection_to_login(page, screenshots_dir)


def close_browser(playwright, browser):
    handle_close_browser(playwright, browser)


def perform_test(page: Page, screenshots_dir: str):
    """Perform the login, capture screenshots, and perform logout for all users."""
    # Load login credentials from the JSON file
    json_login_data = load_login_data()

    # Loop through all users in the JSON data
    for user in json_login_data['users']:
        username = user['username']
        password = user['password']
        expected = user['expected']

        # Navigate to login page
        navigate_to_login_page(page)
        capture_screenshot(page, screenshots_dir, f"before_login_{username}.png")

        try:
            # Perform login with the loaded credentials
            perform_login_with_jason_data(page, username, password)
            capture_screenshot(page, screenshots_dir, f"after_login_{username}.png")

            # Check if the login should be successful
            if expected == "success":
                # If expected success, perform logout
                perform_logout(page)
                capture_screenshot(page, screenshots_dir, f"after_logout_{username}.png")
                # Verify redirection to login page after logout
                perform_logout_redirection_to_login(page, screenshots_dir)
            else:
                # If expected failure, check for failure conditions
                page.wait_for_timeout(2000)  # Wait for a moment to see the outcome
                # Example: Check for an error message on the page
                assert page.is_visible("text='Invalid credentials'"), "Expected error message not found."

        except Exception as e:
            print(f"Error during login attempt for user {username}: {str(e)}")
            capture_screenshot(page, screenshots_dir, f"error_{username}.png")

        # Wait before proceeding to the next user
        page.wait_for_timeout(3000)  # Wait for 3 seconds before the next login attempt


def test_all_users_login():
    """Main test function to perform login and logout for all users."""
    playwright, browser, page = setup_browser()  # This will default to headless=False
    screenshots_dir = setup_screenshot_directory()

    try:
        perform_test(page, screenshots_dir)
    except Exception as e:
        print(f"Error during login/logout tests: {str(e)}")
        capture_screenshot(page, screenshots_dir, "error.png")
        raise
    finally:
        close_browser(playwright, browser)


# Entry point for running the tests directly
if __name__ == "__main__":
    test_all_users_login()
