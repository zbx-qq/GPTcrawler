from fastapi import FastAPI
from api.crawlerRequest import router
from config.middleware import SimpleInterceptor  #拦截器
import uvicorn
from config.logger import logger
app = FastAPI()

# 正确添加中间件
app.add_middleware(SimpleInterceptor)

app.include_router(router)

if __name__ == "__main__":
    logger.info("应用启动中...")
    uvicorn.run(app=app, host="0.0.0.0", port=8080)
