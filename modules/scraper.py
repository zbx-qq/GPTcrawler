import asyncio
import json
from playwright.async_api import async_playwright
from config.logger import logger


# cookieIndex = 0
#
# # ---- 加载 cookies（一次性） ----
# with open('data/cookies.json', 'r', encoding='utf-8') as f:
#     ALL_COOKIES = json.load(f)
#     for cookie in ALL_COOKIES:
#         cookie["value"] = cookie["value"].replace("\t", "").replace("\n", "")


async def crawler(problem_list,click,cookie):
    # global cookieIndex
    responses = []

    async with async_playwright() as p:


        browser = await p.chromium.launch(
            headless=False,
            executable_path="/data/opt/google/chrome/chrome",
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-blink-features=AutomationControlled',
            ]
        #设置代理
        # args = [
        #     "--no-sandbox",
        #     "--disable-setuid-sandbox",
        #     "--disable-blink-features=AutomationControlled",
        #     "--proxy-server=https://131.0.0.1:7890"  # <-- 通过 args 设置代理
        # ]
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 743},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        )

        # 设置 Cookie
        # cookie = ALL_COOKIES[cookieIndex % len(ALL_COOKIES)]
        # cookieIndex += 1
        # logger.info(f"当前使用第 {cookieIndex} 个 Cookie")
        await context.add_cookies(cookie)

        page = await context.new_page()

        # 拦截响应
        page.on("response", lambda response: asyncio.ensure_future(handle_response(response, responses)))

        # 访问 ChatGPT 网站
        await page.goto("https://chatgpt.com", wait_until="networkidle")
        await asyncio.sleep(6)

        # 判断是否弹窗存在登录按钮
        login_button = await page.query_selector('button:has-text("登录")')  # 也可以改成英文 "Log in" 看页面语言
        if login_button:
            logger.error("检测到登录按钮，说明未登录或cookie无效")
            raise Exception("登录失败：cookie 无效或已过期")
        logger.info("未检测到登录弹窗，视为登录成功")

        if click:
           try:
               await page.get_by_role("button", name="工具").click(timeout=10000)
               logger.info(f"工具按钮点击成功")
           except Exception as e:
               logger.info(f"工具按钮点击失败：",e)


           # 点击“网页搜索”菜单项
           try:
               await page.get_by_text("网页搜索").click(timeout=10000)
               logger.info("点击“网页搜索”菜单项成功")
               await asyncio.sleep(3)
           except Exception as e:
               logger.info("网页搜索菜单点击失败",e)

        # 输入问题并提交
        for q in problem_list:
            await page.type("textarea", q)
            await asyncio.sleep(1)
            await page.keyboard.press("Enter")
            await asyncio.sleep(25)

        await browser.close()
        return responses


# ---- 拦截 conversation 相关响应 ----
async def handle_response(response, responses):
    try:
        url = response.url
        if "conversation" in url and response.request.method == "POST":
            body = await response.text()
            payload = response.request.post_data
            responses.append({
                "url": url,
                "body": body,
                "payload": payload
            })
    except Exception as e:
        print("响应处理出错：", e)
