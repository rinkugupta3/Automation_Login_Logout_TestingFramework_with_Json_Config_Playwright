# pytest tests_headless_false/test_login_headless_false_config_data.py --browser=chromium
# pytest tests_headless_false/test_login_headless_false_config_data.py --browser=firefox
# pytest tests_headless_false/test_login_headless_false_config_data.py --browser=webkit
# pytest tests_headless_false/test_login_headless_false_config_data.py
# pytest tests_headless_false/test_login_headless_false_config_data.py --html=reportdbb.html

# pytest tests_headless_false/test_login_headless_false_config_data.py --html=<put html report file name.html>
# pytest tests_headless_false/test_login_headless_false_config_data.py --html=report-headless-false-ConfigData.html


"""
Run test with following command as will generate complete logs in reportdbb.html file
# pytest tests/test_login_headless_false_config_data.py --html=reportdbb.html

"""

import os
import logging
import pytest
from playwright.sync_api import sync_playwright, Page
from config.config import Config
from modules.close_browser import handle_close_browser
from modules.navigate_to_login_page import handle_navigate_to_login_page
from modules.perform_login_with_config_data import handle_perform_login_with_config_data
from modules.perform_logout import handle_perform_logout
from modules.perform_logout_redirection_to_login import handle_perform_logout_redirection_to_login

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


def setup_screenshot_directory(browser_name):
    """Set up the directory to store screenshots for the specified browser."""
    screenshots_dir = f'screenshots/{browser_name}'
    os.makedirs(screenshots_dir, exist_ok=True)
    return screenshots_dir


def capture_screenshot(page: Page, screenshots_dir: str, filename: str):
    """Capture a screenshot and save it to the specified directory."""
    logger.info(f"Capturing screenshot: {filename}")
    page.screenshot(path=os.path.join(screenshots_dir, filename))


def setup_browser(browser_name: str, headless=False):
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


def perform_login_with_config_data(page, username, password):
    logger.info(f"Performing login for user: {username}")
    handle_perform_login_with_config_data(page, username, password)


def perform_test(page: Page, screenshots_dir: str, browser_name: str):
    """Perform the login, capture screenshots, and perform logout for all users."""
    for user in Config.USERS:
        username = user['username']
        password = user['password']

        logger.info(f"Starting login/logout test for user: {username}")

        # Navigate to login page and wait for it to load
        navigate_to_login_page(page)
        capture_screenshot(page, screenshots_dir, f"before_login_{username}.png")

        try:
            # Perform login with the loaded credentials
            perform_login_with_config_data(page, username, password)
            capture_screenshot(page, screenshots_dir, f"after_login_{username}.png")

            # Check if the login was successful
            if page.url == 'https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index':
                logger.info(f"Login successful for user: {username}")
                # Perform logout and capture a screenshot
                perform_logout(page)
                page.wait_for_url(Config.BASE_URL, timeout=30000)
                capture_screenshot(page, screenshots_dir, f"after_logout_{username}.png")
            else:
                logger.warning(f"Login failed for user {username}. Staying on login page.")
                capture_screenshot(page, screenshots_dir, f"login_failed_{username}.png")

        except Exception as e:
            logger.error(f"Error during login/logout tests for user {username}: {str(e)}")
            capture_screenshot(page, screenshots_dir, f"error_{username}.png")
            raise


def test_login_with_config_data():
    """Test login and logout for multiple users using Playwright's page fixture."""
    # Use a list of browser names
    browser_names = ["chromium", "firefox", "webkit"]

    # Loop through each browser and perform tests
    for browser_name in browser_names:
        headless_mode = False  # Set this to False to see the browsers open
        logger.info(f"Testing with {browser_name}...")

        # Set up the browser and the corresponding screenshot directory
        screenshots_dir = setup_screenshot_directory(browser_name)
        playwright, browser, page = setup_browser(browser_name, headless=headless_mode)

        try:
            # Perform the test for the specific browser
            perform_test(page, screenshots_dir, browser_name)
        except Exception as e:
            logger.error(f"Error during login/logout tests with {browser_name}: {str(e)}")
            capture_screenshot(page, screenshots_dir, f"error.png")
            raise
        finally:
            close_browser(playwright, browser)
