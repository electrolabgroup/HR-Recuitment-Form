import asyncio
from playwright.async_api import async_playwright
import os
from pathlib import Path

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Launch the browser (set headless=False to see the browser)
        page = await browser.new_page()
        pdf_folder = Path(r"C:\Users\Sayadf\Another Quarter\HR Recuitment Form\Resume_Upload")

        pdf_files = [file.stem  for file in pdf_folder.glob("*.pdf")]

        # Go to the login page
        await page.goto("https://erpv14.electrolabgroup.com/login#login")

        # Define login credentials
        email_address = "slaadmin"
        password = "slaadmin@123"

        # Fill in the login form
        await page.fill("#login_email", email_address)
        await page.fill("#login_password", password)

        # Click the login button
        await page.click(".btn-login")

        await page.wait_for_timeout(6000)

        for pdf in pdf_files:
            pdf_name = pdf  
            target_url = f"https://erpv14.electrolabgroup.com/app/job-applicant/{pdf_name}"

            await page.goto(target_url)
            await page.wait_for_timeout(2000)  

            await page.click("span.pill-label.ellipsis:has-text('Attach File')")
            await page.wait_for_timeout(2000)  

            file_path = str(pdf_folder / f"{pdf_name}.pdf")
            await page.wait_for_timeout(2000)  


            file_input_selector = "input[type='file']"  
            await page.set_input_files(file_input_selector, file_path)
            await page.wait_for_timeout(3000)  

            await page.click("button[type='button'].btn.btn-primary.btn-sm.btn-modal-primary")

            await page.wait_for_timeout(5000)

        await browser.close()

asyncio.run(run())
