from playwright.sync_api import Page
from logger import logger

def go_to_clients(page: Page):
    """
    Navigates to the Clients section.
    
    Args:
        page (Page): The Playwright page object.
    """
    logger.info("Navigating to 'Clientes'...")
    
    # Sometimes menu is collapsed or "Cadastros" needs to be clicked first.
    # Previous inspection showed "Clientes" might be inside "Cadastros".
    # We will try to click "Clientes" directly if visible, or expand "Cadastros" first.
    
    try:
        # Try finding 'Clientes' directly
        clientes_link = page.get_by_role("link", name="Clientes", exact=True)
        if clientes_link.is_visible():
            clientes_link.click()
        else:
            # Maybe inside Cadastros (based on some typical admin templates)
            # Inspection showed clicking "Cadastros" might be needed.
            cadastros = page.get_by_text("Cadastros") 
            if cadastros.is_visible():
                cadastros.click()
                # Now try clicking CLIENTES again
                page.get_by_role("link", name="Clientes").click()
            else:
                # Fallback: force navigation via URL if UI fails
                logger.warning("Menu interaction failed, forcing URL navigation.")
                page.goto("https://app.ssotica.com.br/cadastro/cliente")
                
    except Exception as e:
        logger.error(f"Navigation error: {e}. Attempting direct URL fallback.")
        page.goto("https://app.ssotica.com.br/cadastro/cliente")
    
    # Verify we are on the clients page
    page.wait_for_url("**/cadastro/cliente", timeout=10000)
    logger.info("Arrived at Clients page.")
