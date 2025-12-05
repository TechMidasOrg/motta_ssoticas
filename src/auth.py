from playwright.sync_api import Page, expect
from logger import logger

def login(page: Page, email: str, password: str):
    """
    Logs into the SSotica platform.
    
    Args:
        page (Page): The Playwright page object.
        email (str): User email.
        password (str): User password.
    """
    logger.info(f"Navigating to login page...")
    page.goto("https://app.ssotica.com.br/login")
    
    logger.info("Filling credentials...")
    # Using the selectors identified: #email, #senha
    page.fill("#email", email)
    page.fill("#senha", password)
    
    logger.info("Clicking login button...")
    # Selector identified: button.bgBlue
    page.click("button.bgBlue")
    
    # Wait for navigation away from login page
    logger.info("Waiting for navigation away from login...")
    try:
        # Wait until URL does not contain "login"
        page.wait_for_url(lambda url: "login" not in url.lower(), timeout=30000)
        logger.info(f"Login successful. Current URL: {page.url}")
    except Exception as e:
        logger.error(f"Login wait failed. Current URL: {page.url}")
        raise e
