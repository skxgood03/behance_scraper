# main.py
from ui import create_ui
from utils import logger

if __name__ == "__main__":
    logger.info("启动Behance图片爬虫")
    app = create_ui()
    app.launch()