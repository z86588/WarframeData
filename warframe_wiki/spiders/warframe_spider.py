import scrapy
import json
from ..items import WarframeItem
import logging

class WarframeSpider(scrapy.Spider):
    name = 'warframe'
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
            url='https://api.warframestat.us/warframes/?language=en',
            callback=self.parse_en,
            dont_filter=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            meta={'language': 'en'}
        )
        
        # 中文API
        yield scrapy.Request(
            url='https://api.warframestat.us/warframes/?language=zh',
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
            warframes = json.loads(response.body)
            self.logger.info(f"成功获取到 {len(warframes)} 个英文Warframe数据")
            
            # 保存英文数据以供后续合并
            self.en_warframes = {
                str(warframe.get('uniqueName', '')): warframe
                for warframe in warframes
                if not any(keyword in str(warframe.get('uniqueName', '')).lower() 
                          for keyword in ['archwing'])
            }
            
        except json.JSONDecodeError as e:
            self.logger.error(f"解析英文JSON数据失败: {str(e)}")
            self.logger.debug(f"响应内容: {response.text[:200]}...")
        except Exception as e:
            self.logger.error(f"处理英文数据时出错: {str(e)}")

    def parse_zh(self, response):
        """处理中文数据并与英文数据合并"""
        try:
            warframes = json.loads(response.body)
            self.logger.info(f"成功获取到 {len(warframes)} 个中文Warframe数据")
            
            # 创建中文数据字典
            zh_warframes = {
                str(warframe.get('uniqueName', '')): warframe
                for warframe in warframes
                if not any(keyword in str(warframe.get('uniqueName', '')).lower() 
                          for keyword in ['archwing'])
            }
            
            # 合并中英文数据
            for unique_id, en_warframe in self.en_warframes.items():
                zh_warframe = zh_warframes.get(unique_id)
                if not zh_warframe:
                    continue
                
                try:
                    item = WarframeItem()
                    
                    # 基础信息
                    item['id'] = unique_id
                    item['name_en'] = en_warframe.get('name', '')
                    item['name_zh'] = zh_warframe.get('name', '')
                    item['description_en'] = en_warframe.get('description', '')
                    item['description_zh'] = zh_warframe.get('description', '')
                    
                    # 属性信息
                    item['health'] = float(en_warframe.get('health', 0))
                    item['shield'] = float(en_warframe.get('shield', 0))
                    item['armor'] = float(en_warframe.get('armor', 0))
                    item['energy'] = float(en_warframe.get('power', 0))
                    item['sprint_speed'] = float(en_warframe.get('sprintSpeed', 0))
                    
                    # 技能信息
                    en_abilities = en_warframe.get('abilities', [])
                    zh_abilities = zh_warframe.get('abilities', [])
                    
                    item['abilities_en'] = [
                        {
                            'name': ability.get('name', ''),
                            'description': ability.get('description', '')
                        }
                        for ability in en_abilities
                        if ability.get('name') and ability.get('description')
                    ]
                    
                    item['abilities_zh'] = [
                        {
                            'name': ability.get('name', ''),
                            'description': ability.get('description', '')
                        }
                        for ability in zh_abilities
                        if ability.get('name') and ability.get('description')
                    ]
                    
                    item['passive_en'] = en_warframe.get('passiveDescription', '')
                    item['passive_zh'] = zh_warframe.get('passiveDescription', '')
                    item['mastery_rank'] = int(en_warframe.get('masteryReq', 0))
                    item['polarities'] = en_warframe.get('polarities', [])
                    
                    # 图片和链接
                    item['image_url'] = en_warframe.get('wikiaThumbnail', '')
                    item['wiki_url'] = en_warframe.get('wikiaUrl', '')
                    
                    # 检查必要字段
                    if not (item['name_en'] and item['health'] > 0):
                        self.logger.warning(f"跳过无效的Warframe数据: {en_warframe.get('name', 'unknown')}")
                        continue
                        
                    yield item
                    
                except (ValueError, TypeError) as e:
                    self.logger.warning(f"处理{en_warframe.get('name')}的数值属性时出错: {str(e)}")
                    continue
                
        except json.JSONDecodeError as e:
            self.logger.error(f"解析中文JSON数据失败: {str(e)}")
            self.logger.debug(f"响应内容: {response.text[:200]}...")
        except Exception as e:
            self.logger.error(f"处理中文数据时出错: {str(e)}")

    def closed(self, reason):
        self.logger.info(f'WARFRAME爬虫关闭，原因: {reason}') 