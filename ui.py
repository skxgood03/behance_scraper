# ui.py
import gradio as gr
import time
from typing import Tuple, List, Dict, Any

from scraper import BehanceScraper
from utils import logger


def create_ui():
    """创建Gradio界面"""

    def run_scraper(keyword: str, max_projects: int) -> Tuple[str, str]:
        """执行爬虫的包装函数"""
        progress_text = ""

        def update_progress(text: str):
            nonlocal progress_text
            progress_text += f"{text}\n"

        try:
            start_time = time.time()

            # 创建爬虫实例
            scraper = BehanceScraper(progress_callback=update_progress)

            # 爬取项目列表
            projects, project_urls = scraper.scrape_projects(keyword, max_projects)

            # 爬取项目详情和图片
            image_count = scraper.scrape_details(project_urls)

            # 计算总用时
            total_time = time.time() - start_time
            summary = f"\n任务完成!\n总计爬取 {len(projects)} 个项目，{image_count} 张图片\n用时: {total_time:.2f} 秒"
            update_progress(summary)

            # 格式化结果
            result = "爬取结果:\n"
            for idx, project in enumerate(projects, 1):
                result += f"{idx}. {project['title']}\n   {project['url']}\n"

            return progress_text, result

        except Exception as e:
            error_msg = f"爬取过程出错: {str(e)}"
            logger.error(error_msg)
            update_progress(error_msg)
            return progress_text, ""

    # 创建Gradio界面
    with gr.Blocks(title="Behance图片爬虫", theme=gr.themes.Soft()) as app:
        gr.Markdown("""
        # Behance图片爬虫
        自动从Behance获取指定关键词相关的项目图片。
        """)

        # 主要控制区域：分为左右两栏
        with gr.Row():
            # 左侧：控制面板
            with gr.Column(scale=1):
                gr.Markdown("""### 控制面板""")
                keyword_input = gr.Textbox(
                    label="搜索关键词",
                    placeholder="请输入要搜索的关键词...",
                    value="jetour"
                )
                max_projects = gr.Slider(
                    minimum=1,
                    maximum=50,
                    step=1,
                    value=10,
                    label="最大项目数量"
                )
                submit_btn = gr.Button("开始爬取", variant="primary", size="lg")

            # 右侧：使用说明
            with gr.Column(scale=1):
                gr.Markdown("""
                ### 使用说明
                1. 输入要搜索的关键词
                2. 设置需要爬取的项目数量
                3. 点击"开始爬取"按钮开始运行

                ### 注意事项
                * 关键词使用建议英文，可获得更多结果
                * 请勿频繁爬取，会有封IP风险
                * 图片将保存在所在程序目录的old文件夹中
                """)

        # 进度显示区域：进度和结果并排显示
        with gr.Row():
            with gr.Column():
                progress_output = gr.Textbox(
                    label="爬取进度",
                    lines=15,
                    max_lines=15,
                    autoscroll=True
                )
            with gr.Column():
                result_output = gr.Textbox(
                    label="爬取结果",
                    lines=15,
                    max_lines=15,
                    autoscroll=True
                )

        # 绑定事件
        submit_btn.click(
            fn=run_scraper,
            inputs=[keyword_input, max_projects],
            outputs=[progress_output, result_output]
        )

    return app