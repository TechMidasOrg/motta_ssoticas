from playwright.sync_api import sync_playwright
from auth import login
from utils import handle_popups
from nav import go_to_clients
from client import register_new_client
import os
import argparse
from dotenv import load_dotenv
import random
from logger import logger
from RPA.Robocorp.WorkItems import WorkItems

# Load environment variables
load_dotenv()
# Robocorp WorkItems
# wi = WorkItems()
# wi.get_input_work_item()
# client_name = wi.get_work_item_variable("SEARCH")
# client_phone = wi.get_work_item_variable("PHONE")

def main(keep_open=True, headless=True):
    with sync_playwright() as p:
        # Launch browser (headless by default unless specified)
        browser = p.chromium.launch(headless=headless, args=["--start-maximized"] if not headless else [])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
        
        try:
            # email = os.getenv("EMAIL")
            # password = os.getenv("PASSWORD")
            email = "thiago@techmidas.com.br"
            password = "Motta@123"
            
            if not email or not password:
                raise ValueError("Credentials not found in .env file")

            # 1. Login
            login(page, email, password)
            
            # 2. Handle Dashboard Popups
            handle_popups(page)
            
            # Single Execution
            logger.info("--- Starting Single Execution ---")
            
            # 3. Navigate to Clients
            go_to_clients(page)
            
            # 4. Register New Client
            client_name = "TECHMIDAS9090"
            # Random 11 digits
            phone_number = "61991314343"
            
            # --- Dynamic Unit Selection ---
            # Change this variable to select a different unit
            unit_to_select = "Óticas Motta Aero" 
            # ------------------------------

            mock_obs = (
                f"Paciente: {client_name}\n"
                "Receita: OD -2.00, OE -1.75\n"
                "Intenção: Compra de óculos de grau completo."
            )
            
            logger.info(f"  > Creating client: {client_name}, Phone: {phone_number}, Unit: {unit_to_select}")
            register_new_client(page, client_name, phone_number, observations=mock_obs, unit=unit_to_select)
            
            logger.info("--- Finished Single Execution ---")
            
            logger.info("RPA Process Completed Successfully.")
            
            # User requested to guarantee browser doesn't close
            if keep_open:
                logger.info("Browser remains open. Press Ctrl+C to exit.")
                page.pause()
            else:
                 logger.info("Closing browser...")
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            page.screenshot(path="error_screenshot.png")
            logger.info("Error encountered. Browser open for debugging (if --keep-open).")
            # page.pause() # Removed to prevent Inspector from opening
        finally:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SSotica RPA")
    # User requested to close browser by default now.
    # Logic: if --close is PASSED, we close? Or default close?
    # User said: "Garanta que o browser é fechado".
    # So default behavior should be Close.
    # Let's add a flag --keep-open instead.
    
    parser.add_argument("--keep-open", action="store_true", help="Keep browser open after execution")
    parser.add_argument("--headed", action="store_true", help="Run browser in visible (headed) mode")
    args = parser.parse_args()
    
    should_keep_open = args.keep_open
    is_headless = not args.headed
    
    main(keep_open=should_keep_open, headless=is_headless)
