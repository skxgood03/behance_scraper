# scraper.py
import os
import threading
import time
from typing import Callable, List, Tuple, Dict, Any

from playwright.sync_api import sync_playwright
import requests

from config import PROXY, DOWNLOAD_DIR, SEARCH_URL_TEMPLATE
from utils import logger, get_response, clean_title


class BehanceScraper:
    def __init__(self, progress_callback: Callable[[str], None] = print):
        self.progress_callback = progress_callback

    def log_progress(self, message: str):
        """记录进度并通过回调函数反馈"""
        logger.info(message)
        self.progress_callback(message)

    def scrape_projects(self, keyword: str, max_projects: int = 10, scroll_delay: float = 1.5) -> Tuple[
        List[Dict[str, Any]], List[str]]:
        """爬取Behance项目列表"""
        url = SEARCH_URL_TEMPLATE.format(keyword)
        projects = []
        seen_urls = set()

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                # 设置浏览器上下文
                context_options = {
                    "viewport": {"width": 1920, "height": 1080},
                    "proxy": PROXY
                }
                context = browser.new_context(**context_options)
                page = context.new_page()

                # 访问搜索页面
                self.log_progress(f"访问页面: {url}")
                page.goto(url)
                page.wait_for_load_state("networkidle")

                count = 0
                self.log_progress(f"开始爬取，目标数量: {max_projects} 个项目")

                while count < max_projects:
                    links = page.locator("a.ProjectCoverNeue-coverLink-U39").all()
                    self.log_progress(f"当前页面上找到 {len(links)} 个项目")

                    new_found = False
                    for link in links:
                        href = link.get_attribute("href")
                        title = link.get_attribute("title")

                        if href and href.startswith("/"):
                            href = f"https://www.behance.net{href}"

                        if not href or href in seen_urls:
                            continue

                        clean_text = clean_title(title)
                        projects.append({
                            "title": clean_text,
                            "url": href,
                        })
                        seen_urls.add(href)
                        new_found = True
                        count += 1
                        self.log_progress(f"[{count}/{max_projects}] 找到项目: {clean_text}")

                        if count >= max_projects:
                            break

                    if count >= max_projects:
                        break

                    if not new_found and count < max_projects:
                        self.log_progress(f"滚动加载更多内容... 当前: {count}/{max_projects}")
                        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        time.sleep(scroll_delay)

                        retry_count = 0
                        while retry_count < 5 and not new_found:
                            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                            time.sleep(scroll_delay)
                            retry_count += 1

                        if retry_count >= 5:
                            self.log_progress("已到达内容底部，无法加载更多项目")
                            break

            finally:
                browser.close()

        self.log_progress(f"项目列表爬取完成! 共获取 {len(projects)} 个项目")
        return projects, [p['url'] for p in projects]

    def scrape_details(self, urls: List[str]) -> int:
        """爬取项目详情页的图片"""
        total_images = 0

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                context_options = {
                    "viewport": {"width": 1920, "height": 1080},
                    "proxy": PROXY
                }
                context = browser.new_context(**context_options)
                page = context.new_page()

                for url in urls:
                    try:
                        self.log_progress(f"访问详情页: {url}")
                        page.goto(url)
                        page.wait_for_load_state("networkidle")

                        links = page.locator("img.ImageElement-image-SRv").all()
                        self.log_progress(f"当前页面上找到 {len(links)} 个图片")

                        image_urls = []
                        for link in links:
                            src = link.get_attribute("src")
                            if src:
                                image_urls.append(src)
                                total_images += 1

                        if image_urls:
                            self._download_images(image_urls)

                        time.sleep(2)

                    except Exception as e:
                        self.log_progress(f"处理页面 {url} 时出错: {str(e)}")

            finally:
                browser.close()

        return total_images

    def _download_images(self, image_urls: List[str]):
        """多线程下载图片"""
        threads = []
        for img_url in image_urls:
            t = threading.Thread(target=self._download_single_image, args=(img_url,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def _download_single_image(self, img_url: str):
        """下载单张图片"""
        try:
            img_name = img_url.split('/')[-1]
            response = get_response(img_url, PROXY)

            os.makedirs(DOWNLOAD_DIR, exist_ok=True)
            with open(os.path.join(DOWNLOAD_DIR, img_name), 'wb') as f:
                f.write(response.content)

            self.log_progress(f">> {img_name}下载成功")

        except Exception as e:
            self.log_progress(f"下载图片 {img_url} 失败: {str(e)}")