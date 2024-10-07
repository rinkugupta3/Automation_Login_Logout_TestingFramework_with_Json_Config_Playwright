from playwright.sync_api import Page, Playwright


def handle_navigate_to_login_page(page: Page):
    """ Navigate to the login page and ensure it's fully loaded. """
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    # page.goto('https://opensource-demo.orangehrmlive.com/auth/login')
    page.wait_for_selector('input[name="username"]', timeout=10000)