
gpt_auto_scraper/
│
├── main.py                      # 主流程入口
├── config.py                    # 配置文件（cookies 路径、代理、延迟等）
│
├── modules/
│   ├── __init__.py
│   ├── scraper.py               # 对话内容发送与拦截
│   ├── storage.py               # 存储爬取内容到本地
│   └── scheduler.py             # 定时任务模块（可选）
│
├── data/
│   ├── cookies.json             # 所有账号的cookie
│   ├── contentList              # 提问内容列表（每行为一条）
│   └── conversation_responses.txt  # 爬取内容结果
│
└── README.md                    # 使用说明文档