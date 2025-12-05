from playwright.sync_api import Page
from logger import logger

def handle_popups(page: Page):
    """
    Registers automatic handlers for known popups.
    
    Args:
        page (Page): The Playwright page object.
    """
    try:
        # Define handler for OneSignal popup
        def on_onesignal(locator):
            logger.info("OneSignal popup detected by handler. Dismissing...")
            locator.click()
            # Wait for the container to actually disappear to avoid interception of subsequent clicks
            try:
                page.locator("#onesignal-slidedown-container").wait_for(state="hidden", timeout=3000)
            except:
                logger.warning("Timed out waiting for OneSignal container to hide.")

        # Register the handler
        # When #onesignal-slidedown-cancel-button is visible, click it.
        page.add_locator_handler(
            page.locator("#onesignal-slidedown-cancel-button"),
            on_onesignal
        )
        logger.info("Registered OneSignal popup handler.")
            
    except Exception as e:
        logger.warning(f"Issue registering popup handler: {e}")

    # Add other popup handlers here if discovered
