import asyncio
import json
from pyppeteer import launch

async def crawler(problem: list):
    browser = None
    responses = []

    async def intercept_response(response):
        try:
            url = response.url
            if "conversation" in url and response.request.method == 'POST':
                text = await response.text()
                responses.append({
                    "url": url,
                    "body": text
                })
        except Exception as e:
            print(f"响应处理错误: {e}")

    try:
        # args = ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled',
        #    代理地址→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→→  '--proxy-server=http://xxxx:8080']
        browser = await launch(
            headless=False,
            executablePath='/data/opt/google/chrome/chrome',   #本地浏览器路径
            args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled']
        )

        page = await browser.newPage()
        await page.setViewport({'width': 1280, 'height': 743})
        page.on('response', lambda resp: asyncio.ensure_future(intercept_response(resp)))

        await page.evaluateOnNewDocument(
            'Object.defineProperty(navigator, "webdriver", {get: () => undefined})')
        # windows  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        await page.setUserAgent(
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
        )

        await page.goto('https://chatgpt.com/', {'waitUntil': 'networkidle2'})

        with open('data/cookies.json', 'r', encoding='utf-8') as f:
            cookies = json.load(f)
            for cookie in cookies:
                cookie["value"] = cookie["value"].replace("\t", "").replace("\n", "")
            await page.setCookie(*cookies)

        await page.goto('https://chatgpt.com/', {'waitUntil': 'networkidle2'})

        # with open('data/contentList', 'r', encoding='utf-8') as f:
        #     lists = f.readlines()

        for x in problem:
            await asyncio.sleep(6)
            await page.type('textarea', x)
            await asyncio.sleep(8)
            await page.keyboard.press('Enter')
            await asyncio.sleep(25)

        return responses  # 返回响应数据

    except Exception as e:
        print(f"发生错误: {e}")
        return []
    finally:
        if browser:
            await browser.close()


