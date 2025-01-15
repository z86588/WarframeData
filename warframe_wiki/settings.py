import os
from datetime import datetime

BOT_NAME = 'warframe_wiki'

SPIDER_MODULES = ['warframe_wiki.spiders']
NEWSPIDER_MODULE = 'warframe_wiki.spiders'

# 日志设置
LOG_LEVEL = 'INFO'
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
LOG_FILE = os.path.join(log_dir, f'warframe_wiki_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

# 爬虫设置
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
DOWNLOAD_DELAY = 2
DOWNLOAD_TIMEOUT = 30

# 重试设置
RETRY_ENABLED = True
RETRY_TIMES = 10
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429, 403]
RETRY_PRIORITY_ADJUST = -1

# 请求头设置
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

# 自定义User-Agent
USER_AGENT = 'warframe_wiki (+https://warframe.fandom.com)'

# 数据库设置
DATABASE_URL = 'sqlite:///warframe_wiki/warframe.db'

# 启用的中间件
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# 启用的管道
ITEM_PIPELINES = {
    'warframe_wiki.pipelines.WarframeWikiPipeline': 300,
}

# 禁用Cookie
COOKIES_ENABLED = False

# 启用自动限速
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Database settings
DATABASE_URL = 'sqlite:///warframe_data.db'

# API Settings
WARFRAME_API_URL = 'https://api.warframestat.us'

# Web Interface Settings
WEB_HOST = '127.0.0.1'
WEB_PORT = 8080 