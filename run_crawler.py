import sys
import os
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from warframe_wiki.spiders.warframe_spider import WarframeSpider
from warframe_wiki.spiders.weapon_spider import WeaponSpider
from warframe_wiki.spiders.mod_spider import ModSpider
from warframe_wiki.web_interface import app
import logging

# 设置日志级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('crawler.log')
    ]
)

def run_spiders():
    process = CrawlerProcess(get_project_settings())
    process.crawl(WarframeSpider)
    process.crawl(WeaponSpider)
    process.crawl(ModSpider)
    process.start()

def run_web():
    app.run(host='127.0.0.1', port=8080, debug=True)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--web':
        run_web()
    else:
        run_spiders() 