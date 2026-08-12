#!/usr/bin/env python3
"""Exploration: test clicking 'Person hinzufügen' for Cleo Baake into 7a I, then verify."""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from itslearning_post_kurstag import login, click_first, OUT_DIR

if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser, its = login(p)
        try:
            cid = 190735  # 7a I
            its.goto(f"https://moin.itslearning.com/CourseParticipantsV2/AddParticipants?CourseID={cid}&selectedTabIndex=0", timeout=20000)
            its.wait_for_timeout(2000)
            its.get_by_text("Filter", exact=True).first.click()
            its.wait_for_timeout(1500)

            li = its.locator("li").filter(has_text="7c")
            target = None
            for i in range(li.count()):
                t = li.nth(i).inner_text().strip()
                if t.startswith("7c"):
                    target = li.nth(i)
            target.click()
            its.wait_for_timeout(1500)

            row = its.locator("li").filter(has_text="Baake, Cleo")
            print("row count:", row.count())
            print("row text:", row.first.inner_text())
            row.first.screenshot(path=f"{OUT_DIR}/exp_06_baake_row_before.png")

            add_link = row.first.get_by_text("Person hinzufügen", exact=False)
            print("add_link count:", add_link.count())
            add_link.first.click()
            its.wait_for_timeout(2000)
            its.screenshot(path=f"{OUT_DIR}/exp_07_after_click.png", full_page=True)

            # check row again
            row2 = its.locator("li").filter(has_text="Baake, Cleo")
            print("row2 count after click:", row2.count())
            if row2.count() > 0:
                print("row2 text:", row2.first.inner_text())
        finally:
            browser.close()
