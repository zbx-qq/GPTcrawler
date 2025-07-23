import json

from modules.scraper import crawler
from fastapi import APIRouter
from pydantic import BaseModel

class CrawlerRequest(BaseModel):
    problem: list

router = APIRouter()

@router.post("/crawler")
async def run_crawler(request: CrawlerRequest):
    result = await crawler(request.problem)
    filtered = [item for item in result if item["url"] == "https://chatgpt.com/backend-api/f/conversation"]
    data = {}

    for i, item in enumerate(filtered):
        key = f"data_{i + 1}"
        body = item.get("body", "")
        lines = body.splitlines()
        parsed = []

        current_event = None  # 当前 event 类型

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
                    data_value = data_str  # 非 JSON 字符串，如 "v1"
                parsed.append({
                    "event": current_event,
                    "data": data_value
                })

        data[key] = parsed

    return {"responses": data,"responses1":filtered}


