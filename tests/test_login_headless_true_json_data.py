# pytest tests/test_login_headless_true_json_data.py
# # pytest tests/test_login_headless_true_json_data.py --html=<put html report file name.html>
# # pytest tests/test_login_headless_true_json_data.py --html=report-headless-true-JsonData.html

import json
import os
import logging
from playwright.sync_api import sync_playwright, Page
from modules.close_browser import handle_close_browser
from modules.navigate_to_login_page import handle_navigate_to_login_page
from modules.perform_login_with_json_data import handle_perform_login_with_json_data
from modules.perform_logout import handle_perform_logout
from modules.perform_logout_redirection_to_login import handle_perform_logout_redirection_to_login
from tests.test_login_with_json_data import perform_login_with_jason_data

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("pytest.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_login_data():
    """Load login data from a JSON file."""
    # Get the absolute path of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the absolute path to the JSON file
    json_file_path = os.path.join(current_dir, '../test_data', 'json_login_data.json')

    # Ensure the file exists before opening
    if not os.path.exists(json_file_path):
        raise FileNotFoundError(f"JSON file not found at {json_file_path}")

    with open(json_file_path) as json_file:
        data = json.load(json_file)

    return data


def setup_screenshot_directory(browser_name):
    """Set up the directory to store screenshots for the specified browser."""
    screenshots_dir = f'screenshots/{browser_name}'
    os.makedirs(screenshots_dir, exist_ok=True)
    return screenshots_dir


def capture_screenshot(page: Page, screenshots_dir: str, filename: str):
    """Capture a screenshot and save it to the specified directory."""
    logger.info(f"Capturing screenshot: {filename}")
    page.screenshot(path=os.path.join(screenshots_dir, filename))


def setup_browser(browser_name: str, headless=True):
    """To make headless True or False update in setup_browser and test_login_with_config_data functions."""
    playwright = sync_playwright().start()
    logger.info(f"Launching {browser_name} browser, headless={headless}")

    if browser_name == "chromium":
        browser = playwright.chromium.launch(headless=headless)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headless)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=headless)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    page = browser.new_page()
    logger.info(f"{browser_name} browser launched successfully")
    return playwright, browser, page


def navigate_to_login_page(page: Page):
    logger.info("Navigating to login page...")
    handle_navigate_to_login_page(page)


def perform_logout(page: Page):
    logger.info("Performing logout...")
    handle_perform_logout(page)


def perform_logout_redirection_to_login(page: Page, screenshots_dir: str):
    logger.info("Performing logout redirection to login page...")
    handle_perform_logout_redirection_to_login(page, screenshots_dir)


def close_browser(playwright, browser):
    logger.info("Closing browser...")
    handle_close_browser(playwright, browser)


def perform_login_with_json_data(page, username, password):
    logger.info(f"Performing login for user: {username}")
    handle_perform_login_with_json_data(page, username, password)


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


def test_login_with_config_data():
    """Test login and logout for multiple users using Playwright's page fixture."""
    # Use a list of browser names
    browser_names = ["chromium", "firefox", "webkit"]

    # Loop through each browser and perform tests
    for browser_name in browser_names:
        headless_mode = True  # Set this to False to see the browsers open
        logger.info(f"Testing with {browser_name}...")

        # Set up the browser and the corresponding screenshot directory
        screenshots_dir = setup_screenshot_directory(browser_name)
        playwright, browser, page = setup_browser(browser_name, headless=headless_mode)

        try:
            # Perform the test for the specific browser
            perform_test(page, screenshots_dir)
        except Exception as e:
            logger.error(f"Error during login/logout tests with {browser_name}: {str(e)}")
            capture_screenshot(page, screenshots_dir, f"error.png")
            raise
        finally:
            close_browser(playwright, browser)

