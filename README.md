

## behance_scraper 项目文档 

**behance_scraper**  是一个用于抓取 Behance 作品信息的 Python 项目。 使用 Gradio 搭建的直观的图形化界面，方便用户方便地搜索、浏览和保存感兴趣的作品。

###  目录结构

```
behance_scraper/
├── main.py  # 主程序入口
├── scraper.py  # 爬虫核心逻辑
├── utils.py  # 工具函数
├── ui.py  # Gradio界面
├── config.py  # 配置文件
├── logs/  # 日志目录
└── old/  # 下载图片保存目录
```

###  使用方法

1. **依赖安装**:

   ```bash
   pip install gradio playwright requests 
   ``` 

2. **安装浏览器**:

   运行以下命令安装 Playwright，并选择 Chromium 浏览器:

   ```bash
   playwright install chromium 
   ```

3. **项目设置**:

   - 创建一个名为 `behance_scraper` 的文件夹
   - 将项目代码分别保存到 `main.py`、`scraper.py`、`utils.py`、`ui.py`、`config.py` 文件中
   - 创建一个名为 `logs` 的文件夹用于存储日志文件。
   - 创建一个名为 `old` 的文件夹，用于保存下载的图片。

4. **运行程序**:

   在项目根目录下运行 `python main.py` 。

5. **访问界面**:

   在浏览器中访问 `http://localhost:7860` 即可使用 Gradio 界面对话。

###  更多功能

详细的功能介绍和使用指南将在后续版本中发布。 


 **注意**: 

收集信息时，请遵守 Behance 的条款和使用规则，并注意用户隐私。


  **持续更新**:

  我们将不断更新项目文档，提供更完善的功能介绍和使用指南。 


