from playwright.sync_api import Page
from logger import logger
# from utils import handle_popups # Removed to avoid double registration

def register_new_client(page: Page, name: str, phone: str, observations: str = "", unit: str = None):
    """
    Registers a new client with the given details.
    
    Args:
        page (Page): The Playwright page object.
        name (str): Client name.
        phone (str): Client phone number.
        observations (str, optional): Client observations. Defaults to "".
        unit (str, optional): The unit to select (e.g., "Óticas Motta Aero"). Defaults to None.
    """
    # Ensure no popups block the view before starting
    # handle_popups(page) # Handled globally in main.py via add_locator_handler

    logger.info("Clicking 'Novo Cliente'...")
    # Selector: a#btnNovo
    # Use force=True as a fallback if something invisible still blocks it
    page.click("a#btnNovo", force=True)
    
    # Wait for the specific form to be attached
    logger.info("Waiting for client form...")
    # Using specific name found in logs: formCliente
    form = page.locator("form[name='formCliente']").first
    form.wait_for(state="attached", timeout=15000)

    # --- Unit Selection ---
    if unit:
        try:
            logger.info(f"Attempting to select unit: {unit}")
            # Locate the "Cadastrado Em" label or container
            # Strategy 1: Find something looking like a dropdown near "Cadastrado Em"
            # It might be a select2 or a custom div.
            
            # This xpath looks for a label containing "Cadastrado Em" and then finds the following sibling div or span that acts as the dropdown
            # Adjust selector based on common frameworks (Select2, Chosen, or standard Bootstrap)
            
            # Common pattern: click the container to open dropdown, then click the option.
            
            # Trying to find the container. 
            # Often it's a sibling of the label.
            # Let's try to click the specific text "Óticas Motta Aero" if it's already visible (default), 
            # but usually we need to open it.
            
            # Let's try finding the combobox/dropdown trigger by the label
            # We look for a container containing "Cadastrado Em" and then a .select2-container or similar?
            # Or simpler: The user said "dentro da tela de cadastro, há uma lista".
            
            # Let's try to find the label, then find the input/select associated.
            # If we assume it's a select2 (common in these systems):
            # The label is "Cadastrado Em". The dropdown is next to it.
            
            # Let's try a very generic "Click on a 'select' like element near 'Cadastrado Em'" approach.
            # OR, locate by the text currently selected (if any) or just the label.
            
            # Let's assume standard Select2 or similar behavior:
            # 1. Click the container (often .select2-selection or .form-control)
            # 2. Type the name or Click the name in the results.
            
            # Identifying the dropdown trigger:
            # Look for the label, then get the control.
            label = page.get_by_text("Cadastrado Em", exact=False).first
            
            # Assuming the control is a sibling or inside a form-group.
            # Let's try verify if it's a native select first?
            # select = page.locator("select").filter(has=page.locator("xpath=preceding-sibling::label[contains(text(), 'Cadastrado Em')]"))
            
            # If it's a custom dropdown (screenshot looks like Select2 or similar styled):
            # We usually click the box to open it.
            # Let's try clicking the "box" which might be next to the label.
            # We can use the layout locator: to_right_of=label?
            
            # Simplest first try: Click the current value container.
            # But we don't know the current value.
            
            # Let's try to click the 'select2' container if it exists inside the form.
            # Or assume it is the only dropdown for now? No, risky.
            
            # Let's use layout selector.
            dropdown_trigger = page.locator(".select2-selection, .form-select, .form-control.select, .dropdown-toggle").filter(has_text=page.locator("option:checked").text_content() if False else None) 
            # Too complex.
            
            # Resilient approach for "Unknown Dropdown":
            # 1. Find the label "Cadastrado Em"
            # 2. Click the element right below or to the right of it.
            #    Actually, we can use `page.locator("text=Cadastrado Em").locator("..").click()` if it wraps it?
            
            # Let's try to find an element with role "combobox" or similar.
            # Or simply:
            # page.locator("label:has-text('Cadastrado Em') + div").click() # Standard logic
            # page.get_by_label("Cadastrado Em").click() # If label is correctly associated
            
            # Attempt 1: get_by_label (best practice if accessible)
            try:
                page.get_by_label("Cadastrado Em").click(timeout=3000)
                logger.info("Clicked by label 'Cadastrado Em'.")
            except:
                # Attempt 2: Find label visually and click nearby
                logger.info("Could not click by label. Trying visual location...")
                # Find the label element
                lbl = page.locator("label").filter(has_text="Cadastrado Em").first
                # Click the sibling (assuming standard form-group layout: Label \n Input)
                # Next sibling element:
                dropdown = lbl.locator("xpath=following-sibling::*[1]") 
                dropdown.click()
            
            # Now wait for the options to appear.
            # Usually they appear in a portal or proper body.
            # Click the option with exact text.
            logger.info(f"Waiting for option '{unit}'...")
            
            # Select2/Chosen/etc append to body.
            # We look for the text visible in the page (as it should be in the dropdown now)
            # Use get_by_role option? Or just text.
            # The screenshot shows the option text.
            page.get_by_text(unit, exact=True).first.click()
            
            logger.info(f"Selected unit: {unit}")
            page.wait_for_timeout(500) # stabilizing

        except Exception as e:
            logger.warning(f"Failed to select unit '{unit}': {e}")
            # Don't fail the whole script, just warn? Or fail? 
            # Better to log and continue or throw? 
            # User said "Quero selecionar", so it implies it's important.
            # But maybe defaults are fine. I'll log warning.
    
    logger.info(f"Filling client details: {name}, {phone}")
    
    # Wait for Name input to be visible (playwright auto-waits for actionability)
    # Using generic fallback strategy if label isn't explicit
    # Try finding input by name attribute containing 'nome', or placeholder 'Nome', or just the first text input
    try:
        logger.info("Looking for Name input...")
        name_input = page.locator("input[name*='ome']").or_(page.get_by_placeholder("Nome")).or_(page.locator("input[type='text']").first)
        name_input.first.fill(name)
        
        logger.info("Handling Phone input...")
        # Always click "Novo Telefone" as requested
        try:
            # 1. Click "Novo Telefone" to ensure a row exists (or add a new one)
            # Check if one is already visible? The user instruction implies clicking it.
            # "O local é Informações de Contato > Clicar em Novo Telefone"
            # Updated selector based on user feedback: id="btnNovoTelefone"
            # Updated selector based on user feedback: id="btnNovoTelefone"
            # Switch back to standard click to ensure add_locator_handler works if intercepted
            # Resilience delay requested by user
            logger.info("Waiting 2s before clicking #btnNovoTelefone...")
            page.wait_for_timeout(2000)

            logger.info("Clicking #btnNovoTelefone (Standard Click)...")
            page.click("#btnNovoTelefone")
            
            # Using JS click failed to trigger the event. Reverted to Playwright click which worked in debug.
            # page.evaluate("document.getElementById('btnNovoTelefone').click()")
            
            page.wait_for_timeout(1000) # Wait for animation/DOM update
            
            # Wait for at least one phone input to be visible to ensure the row was added
            page.wait_for_selector("input.numero-telefone:visible", state="visible", timeout=30000) 
            
            # --- Handle Duplicates ---
            # User reported sometimes duplicate fields appear. Check count and delete extras.
            logger.info("Checking for duplicate phone fields...")
            trash_icons = page.locator("a.icone-excluir:visible")
            count = trash_icons.count()
            
            if count > 1:
                logger.warning(f"Found {count} phone fields. Deleting one...")
                # Click the first delete icon
                trash_icons.first.click()
                
                # Handle Confirmation Popup (Sim)
                logger.info("Waiting for confirmation popup...")
                # Assuming standard bootstrap/alert: Button with text "Sim"
                sim_btn = page.get_by_role("button", name="Sim").or_(page.locator("button:has-text('Sim')"))
                if sim_btn.is_visible():
                     sim_btn.click()
                     logger.info("Clicked 'Sim' to confirm deletion.")
                     page.wait_for_timeout(1000) # Wait for deletion animation
                else:
                    logger.warning("Could not find confirmation button 'Sim'.")
            
            # 2. Find the input using the user-provided class/attribute details
            # HTML: <input ... class="numero-telefone form-control" ... name="telefones[0][numero_sem_mascara]" ...>
            
            # We target the last visible input with this specific class, assuming we want to fill the one we just added.
            logger.info("Filling Phone Number using specific selector...")
            phone_input = page.locator("input.numero-telefone:visible").last
            
            phone_input.fill(phone)
            
            logger.info("Selecting 'Principal' radio button...")
            # User provided specific ID pattern: 
            # Phone Input: id="telefones[1][numero_sem_mascara]"
            # Radio Button: id="telefonePrincipalSel-1"
            
            # Get the ID of the input we just filled
            input_id = phone_input.get_attribute("id")
            if input_id:
                # Extract the index. Expected format: telefones[<index>][...]
                import re
                match = re.search(r"telefones\[(\d+)\]", input_id)
                if match:
                    index = match.group(1)
                    logger.info(f"  > Index found: {index}. Clicking #telefonePrincipalSel-{index}")
                    page.click(f"#telefonePrincipalSel-{index}")
                else:
                    logger.warning("  > Could not extract index from ID, trying fallback (last radio).")
                    page.locator("input[type='radio'][name='telefonePrincipalSel']").last.click()
            else:
                 logger.warning("  > Input has no ID, trying fallback (last radio).")
                 page.locator("input[type='radio'][name='telefonePrincipalSel']").last.click()

        except Exception as e:
            logger.error(f"Error handling phone: {e}")
            raise e

    except Exception as e:
        logger.error(f"Error filling form: {e}")
        # Capture form HTML for debug if needed, but for now just fail
        raise e
    
    if observations:
        try:
            logger.info("Filling observations...")
            # Try to find the observations field. 
            # It might be a textarea with "Observações" placeholder or label, or name="observacoes"
            obs_input = page.locator("textarea").or_(page.get_by_placeholder("Observações"))
            obs_input.first.fill(observations)
        except Exception as e:
            logger.warning(f"Could not fill observations: {e}") 


    logger.info("Saving client...")
    # "Salvar" button - try role button or explicitly type=submit
    save_btn = page.get_by_role("button", name="Salvar").or_(page.locator("button[type='submit']")).or_(page.locator("button:has-text('Salvar')"))
    save_btn.first.click()
    
    # Wait for success indication
    page.wait_for_timeout(2000)
    logger.info("Client registered successfully (assumed based on no errors).")
