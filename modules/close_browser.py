def handle_close_browser(playwright, browser):
    """Ensure the browser and Playwright are properly closed."""
    browser.close()
    playwright.stop()