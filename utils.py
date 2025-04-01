# utils.py
import logging
import os
import random
import time
from datetime import datetime
from pathlib import Path
import requests
from config import USER_AGENTS, LOGS_DIR


def setup_logger() -> logging.Logger:
    """设置日志记录器"""
    # 确保日志目录存在
    Path(LOGS_DIR).mkdir(exist_ok=True)

    # 创建日志文件名(包含时间戳)
    log_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_behance_scraper.log"
    log_filepath = os.path.join(LOGS_DIR, log_filename)

    # 配置日志记录器
    logger = logging.getLogger('behance_scraper')
    logger.setLevel(logging.INFO)

    # 文件处理器
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 添加处理器
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def get_response(url: str, proxy=None, max_retries=4) -> requests.Response:
    """发送HTTP请求并获取响应"""
    headers = {
        'Connection': 'close',
        "User-Agent": random.choice(USER_AGENTS)
    }

    for i in range(max_retries):
        try:
            proxies = {"http": proxy['server'], "https": proxy['server']} if proxy else None
            response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
            return response
        except requests.exceptions.RequestException:
            if i < max_retries - 1:  # 如果不是最后一次重试
                wait_time = (i + 1) * 2
                logger.warning(f"获取网页出错，{wait_time}秒后将重试第{i + 1}次")
                time.sleep(wait_time)
            else:
                raise


def clean_title(title: str) -> str:
    """清理标题文本"""
    if title and "项目的链接 - " in title:
        return title.replace("项目的链接 - ", "")
    return title


# 创建全局logger实例
logger = setup_logger()