from config.config import Config
from playwright.sync_api import Page


def handle_perform_login_with_json_data(page: Page, username: str, password: str):
    """Perform the login action with jason data."""
    page.fill('input[name="username"]', username)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    # Wait until the URL indicates the dashboard and the network is idle
    # page.wait_for_url('https://opensource-demo.orangehrmlive.com/web/index.php/dashboard/index', timeout=30000)
    # page.wait_for_url('https://opensource-demo.orangehrmlive.com/dashboard/index', timeout=30000)
    page.wait_for_load_state('networkidle')