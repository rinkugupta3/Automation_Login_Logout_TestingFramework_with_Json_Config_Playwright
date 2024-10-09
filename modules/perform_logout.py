import os

from playwright.sync_api import Page


def handle_perform_logout(page: Page):
    """ Perform the logout action on the web page."""
    try:
        print("Attempting to find and click on user dropdown...")

        # Locate the user dropdown-----page.locator('span i')
        """
            Locate the user dropdown element by capturing all dropdowns and selecting the right one.
            If there are multiple dropdowns, capture all and then select the one you need based on additional criteria like visibility or position
            selector can be used when the exact text or attributes of the element are not known or are changing dynamically.
            CSS Selector Breakdown
            span: This targets all <span> elements on the page.
            i: This targets all <i> elements that are children of the <span> elements.
        """
        user_dropdown = page.locator('span i')
        if user_dropdown.is_visible():
            user_dropdown.wait_for(state='visible', timeout=10000)
            user_dropdown.click()
            print("User dropdown clicked.")

            page.wait_for_timeout(10000)
            # Click the 'Logout' button
            page.get_by_role('menuitem', name='Logout').click()
            page.wait_for_load_state('networkidle')

        else:
            raise Exception("User dropdown not found.")

    except TimeoutError:
        print("TimeoutError: The element could not be found or interacted with in time.")
        page.screenshot(path=os.path.join('screenshots', 'logout_timeout_error.png'))
        raise
