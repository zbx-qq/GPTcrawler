# modules/storage.py

import json

conversation_responses = []

async def intercept_response(response):
    if 'backend-api/f/conversation' in response.url and response.status == 200:
        try:
            print(f"URL: {response.url}")
            print(f"Status: {response.status}")
            headers = response.headers
            print("Response Headers:")
            for key, value in headers.items():
                print(f"{key}: {value}")
            resp_text = await response.text()
            print("Response Body:")
            try:
                resp_data = json.loads(resp_text)
                conversation_responses.append(json.dumps(resp_data, ensure_ascii=False, indent=2))
            except json.JSONDecodeError:
                conversation_responses.append(resp_text)
        except Exception as e:
            print(f"解析失败: {e}")

def store_responses(path='data/conversation_responses.txt'):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            for i in conversation_responses:
                f.write(i + "\n")
        print(f"对话数据已保存到 {path}")
    except Exception as e:
        print(f"保存文件失败: {e}")
