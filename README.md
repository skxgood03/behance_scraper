behance_scraper/
│
├── main.py           # 主程序入口
├── scraper.py        # 爬虫核心逻辑
├── utils.py          # 工具函数
├── ui.py             # Gradio界面
├── config.py         # 配置文件
├── logs/             # 日志目录
└── old/              # 下载图片保存目录

使用方法：

确保安装了所需的依赖：
pip install gradio playwright requests
运行Playwright安装浏览器：
playwright install chromium
创建上述文件结构，将代码保存到相应的文件中
运行程序：
python main.py
在浏览器中访问 http://localhost:7860 即可使用界面
