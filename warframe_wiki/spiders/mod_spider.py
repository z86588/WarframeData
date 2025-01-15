import scrapy
import json
from ..items import ModItem
import logging
import asyncio
import aiohttp

class ModSpider(scrapy.Spider):
    name = 'mod'
    allowed_domains = ['api.warframestat.us']
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'DOWNLOAD_DELAY': 2,
        'DOWNLOAD_TIMEOUT': 30,
        'ROBOTSTXT_OBEY': False,
        'RETRY_TIMES': 5,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 522, 524, 408, 429],
        'HTTPERROR_ALLOWED_CODES': [404, 429],
    }

    def start_requests(self):
        # 英文API
        yield scrapy.Request(
            url='https://api.warframestat.us/mods/?language=en',
            callback=self.parse_en,
            dont_filter=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            meta={'language': 'en'}
        )
        
        # 中文API
        yield scrapy.Request(
            url='https://api.warframestat.us/mods/?language=zh',
            callback=self.parse_zh,
            dont_filter=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            meta={'language': 'zh'}
        )

    def parse_en(self, response):
        """处理英文数据"""
        try:
            mods = json.loads(response.body)
            self.logger.info(f"成功获取到 {len(mods)} 个英文Mod数据")
            
            # 保存英文数据以供后续合并
            self.en_mods = {
                str(mod.get('uniqueName', '')): mod
                for mod in mods
            }
            
        except json.JSONDecodeError as e:
            self.logger.error(f"解析英文JSON数据失败: {str(e)}")
            self.logger.debug(f"响应内容: {response.text[:200]}...")
        except Exception as e:
            self.logger.error(f"处理英文数据时出错: {str(e)}")

    def parse_zh(self, response):
        """处理中文数据并与英文数据合并"""
        try:
            mods = json.loads(response.body)
            self.logger.info(f"成功获取到 {len(mods)} 个中文Mod数据")
            
            # 创建中文数据字典
            zh_mods = {
                str(mod.get('uniqueName', '')): mod
                for mod in mods
            }
            
            # 合并中英文数据
            for unique_id, en_mod in self.en_mods.items():
                zh_mod = zh_mods.get(unique_id)
                if not zh_mod:
                    continue
                
                item = ModItem()
                
                # 基础信息
                item['id'] = unique_id
                item['name_en'] = en_mod.get('name', '')
                item['name_zh'] = zh_mod.get('name', '')
                item['description_en'] = en_mod.get('description', '')
                item['description_zh'] = zh_mod.get('description', '')
                item['polarity'] = en_mod.get('polarity', '')
                item['rarity'] = en_mod.get('rarity', '')
                item['drain'] = int(en_mod.get('baseDrain', 0))
                item['max_rank'] = int(en_mod.get('fusionLimit', 0))
                
                # 效果
                item['effect_en'] = en_mod.get('levelStats', [{}])[0].get('stats', [''])[0] if en_mod.get('levelStats') else ''
                item['effect_zh'] = zh_mod.get('levelStats', [{}])[0].get('stats', [''])[0] if zh_mod.get('levelStats') else ''
                
                # 图片和链接
                item['image_url'] = en_mod.get('wikiaThumbnail', '')
                item['wiki_url'] = en_mod.get('wikiaUrl', '')
                
                # 检查必要字段
                if not (item['name_en'] and item['id']):
                    self.logger.warning(f"跳过无效的Mod数据: {en_mod.get('name', 'unknown')}")
                    continue
                    
                yield item
                
        except json.JSONDecodeError as e:
            self.logger.error(f"解析中文JSON数据失败: {str(e)}")
            self.logger.debug(f"响应内容: {response.text[:200]}...")
        except Exception as e:
            self.logger.error(f"处理中文数据时出错: {str(e)}")

    def closed(self, reason):
        self.logger.info(f'MOD爬虫关闭，原因: {reason}') 