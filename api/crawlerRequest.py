import json

from starlette.responses import JSONResponse
from modules.scraper import crawler
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
class CrawlerRequest(BaseModel):
    problem: list
    click:bool
    cookie:list

router = APIRouter()

@router.post("/crawler")
async def run_crawler(request: CrawlerRequest):
    try:
        result = await crawler(request.problem, request.click, request.cookie)
    except Exception as e:
        return JSONResponse(
            status_code=401,
            content={
                "error": "登录失败",
                "message": str(e)
            }
        )

    filtered = [item for item in result if item["url"] == "https://chatgpt.com/backend-api/f/conversation"]

    response_data = []

    for i, item in enumerate(filtered):
        question_text = request.problem[i] if i < len(request.problem) else f"question_{i + 1}"
        body = item.get("body", "")
        payload = json.loads(item.get("payload", ""))
        lines = body.splitlines()
        parsed = []

        current_event = None

        for line in lines:
            line = line.strip()
            if line.startswith("event:"):
                current_event = line[len("event:"):].strip()
            elif line.startswith("data:"):
                data_str = line[len("data:"):].strip()
                if data_str == "[DONE]":
                    continue
                try:
                    data_value = json.loads(data_str)
                except json.JSONDecodeError:
                    data_value = data_str
                parsed.append({
                    "event": current_event,
                    "data": data_value
                })

        response_data.append({
            "question": question_text,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "payload": payload,
            "answer": parsed,
        })

    return response_data
