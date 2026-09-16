import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        console_msgs = []
        page.on("console", lambda msg: console_msgs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda exc: console_msgs.append(f"[pageerror] {exc}"))

        await page.goto("http://127.0.0.1:18790/", wait_until="networkidle")
        # navigate to KI-Forum via nav item
        await page.click('[data-page="kiforum"]')
        await page.wait_for_timeout(1500)

        print("=== nach Seitenwechsel ===")
        for m in console_msgs: print(m)
        console_msgs.clear()

        # click Neu laden
        reload_btn = page.locator('button.kif-topbtn', has_text="Neu laden")
        print("reload btn count:", await reload_btn.count())
        await reload_btn.click()
        await page.wait_for_timeout(1500)
        print("=== nach Neu laden Klick ===")
        for m in console_msgs: print(m)
        console_msgs.clear()

        await browser.close()

asyncio.run(main())
