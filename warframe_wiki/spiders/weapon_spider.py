import scrapy
import json
from ..items import WeaponItem
import logging

class WeaponSpider(scrapy.Spider):
    name = 'weapon'
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
            url='https://api.warframestat.us/weapons/?language=en',
            callback=self.parse_en,
            dont_filter=True,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            },
            meta={'language': 'en'}
        )
        
        # 中文API
        yield scrapy.Request(
            url='https://api.warframestat.us/weapons/?language=zh',
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
            weapons = json.loads(response.body)
            self.logger.info(f"成功获取到 {len(weapons)} 个英文武器数据")
            
            # 保存英文数据以供后续合并
            self.en_weapons = {
                str(weapon.get('uniqueName', '')): weapon
                for weapon in weapons
            }
            
        except json.JSONDecodeError as e:
            self.logger.error(f"解析英文JSON数据失败: {str(e)}")
            self.logger.debug(f"响应内容: {response.text[:200]}...")
        except Exception as e:
            self.logger.error(f"处理英文数据时出错: {str(e)}")

    def parse_zh(self, response):
        """处理中文数据并与英文数据合并"""
        try:
            weapons = json.loads(response.body)
            self.logger.info(f"成功获取到 {len(weapons)} 个中文武器数据")
            
            # 创建中文数据字典
            zh_weapons = {
                str(weapon.get('uniqueName', '')): weapon
                for weapon in weapons
            }
            
            # 合并中英文数据
            for unique_id, en_weapon in self.en_weapons.items():
                zh_weapon = zh_weapons.get(unique_id)
                if not zh_weapon:
                    continue
                
                item = WeaponItem()
                
                # 基础信息
                item['id'] = unique_id
                item['name_en'] = en_weapon.get('name', '')
                item['name_zh'] = zh_weapon.get('name', '')
                item['description_en'] = en_weapon.get('description', '')
                item['description_zh'] = zh_weapon.get('description', '')
                item['type'] = en_weapon.get('type', '')
                item['mastery_rank'] = int(en_weapon.get('masteryReq', 0))
                
                # 伤害相关
                try:
                    damage_data = {
                        'impact': float(en_weapon.get('damageTypes', {}).get('impact', 0)),
                        'puncture': float(en_weapon.get('damageTypes', {}).get('puncture', 0)),
                        'slash': float(en_weapon.get('damageTypes', {}).get('slash', 0)),
                        'total': float(en_weapon.get('totalDamage', 0))
                    }
                    item['damage'] = json.dumps(damage_data)
                except (ValueError, TypeError, AttributeError) as e:
                    self.logger.warning(f"处理武器 {en_weapon.get('name')} 的伤害数据时出错: {str(e)}")
                    item['damage'] = json.dumps({'impact': 0, 'puncture': 0, 'slash': 0, 'total': 0})
                
                # 其他属性
                item['critical_chance'] = float(en_weapon.get('criticalChance', 0))
                item['critical_multiplier'] = float(en_weapon.get('criticalMultiplier', 0))
                item['status_chance'] = float(en_weapon.get('procChance', 0))
                
                # 图片和链接
                item['image_url'] = en_weapon.get('wikiaThumbnail', '')
                item['wiki_url'] = en_weapon.get('wikiaUrl', '')
                
                # 检查必要字段
                if not (item['name_en'] and item['id']):
                    self.logger.warning(f"跳过无效的武器数据: {en_weapon.get('name', 'unknown')}")
                    continue
                    
                yield item
                
        except json.JSONDecodeError as e:
            self.logger.error(f"解析中文JSON数据失败: {str(e)}")
            self.logger.debug(f"响应内容: {response.text[:200]}...")
        except Exception as e:
            self.logger.error(f"处理中文数据时出错: {str(e)}")

    def closed(self, reason):
        self.logger.info(f'WEAPON爬虫关闭，原因: {reason}') 