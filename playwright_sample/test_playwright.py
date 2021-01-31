import time

from playwright import sync_playwright

# 以下コマンドラインでレコード機能
# python -m playwright codegen

def test_run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.newContext()

    page = context.newPage()

    # Go to
    page.goto("https://next.rikunabi.com/")

    # ScreenShot 1
    page.screenshot(path="playwright1.png")

    # Click
    page.click("text=\"ログイン\"")

    # Fill input
    page.fill("input[name=\"mainEmail\"]", "sample@foo.bar")
    # Fill input
    page.fill("input[name=\"passwd\"]", "passwordtest")

    # Click
    page.click("text=\"上記に同意してログイン\"")

    # ScreenShot 2
    page.screenshot(path="playwright2.png")

    # その他情報
    # page.check("#music") #チェックボックス
    # page.selectOption("input[name=\"age\"]", "24") #プルダウン
    # assert "パスワード不正" in page.innerText("#error_message")

    time.sleep(4)

    # Close page
    page.close()

    context.close()
    browser.close()

with sync_playwright() as playwright:
    test_run(playwright)
