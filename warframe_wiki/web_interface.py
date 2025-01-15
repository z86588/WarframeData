from flask import Flask, send_from_directory, jsonify, request, make_response, render_template
from .database import init_db, Warframe, Weapon, Mod
import logging
from datetime import datetime
from sqlalchemy import func
import os
import json
from sqlalchemy.orm import scoped_session
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from .spiders.warframe_spider import WarframeSpider
from .spiders.weapon_spider import WeaponSpider
from .spiders.mod_spider import ModSpider
import multiprocessing
import time

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, 'static')

app = Flask(__name__, static_url_path='', static_folder=static_dir)

# 创建数据库会话工厂
Session = scoped_session(init_db)

# 全局变量用于追踪爬虫状态
crawler_status = {
    'is_running': False,
    'last_run': None,
    'message': '',
    'current_type': None
}

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

def get_db():
    return Session()

# 确保日志目录存在
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

def no_cache_response(response):
    """添加无缓存头部"""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/')
def index():
    response = make_response(send_from_directory(app.static_folder, 'index.html'))
    return no_cache_response(response)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory(os.path.join(app.static_folder, 'js'), path)

@app.route('/api/stats')
def get_stats():
    """获取数据库统计信息"""
    db = None
    try:
        db = get_db()
        stats = {
            'warframes': {
                'count': db.query(func.count(Warframe.id)).scalar(),
                'last_updated': db.query(func.max(Warframe.last_updated)).scalar()
            },
            'weapons': {
                'count': db.query(func.count(Weapon.id)).scalar(),
                'last_updated': db.query(func.max(Weapon.last_updated)).scalar()
            },
            'mods': {
                'count': db.query(func.count(Mod.id)).scalar(),
                'last_updated': db.query(func.max(Mod.last_updated)).scalar()
            }
        }
        
        # 格式化时间
        for category in stats.values():
            if category['last_updated']:
                category['last_updated'] = category['last_updated'].strftime('%Y-%m-%d %H:%M:%S')
        
        response = jsonify({'success': True, 'data': stats})
        return no_cache_response(response)
    except Exception as e:
        app.logger.error(f"获取统计信息失败: {str(e)}")
        if db:
            db.rollback()
        response = jsonify({'success': False, 'error': str(e)})
        return no_cache_response(response)
    finally:
        if db:
            db.close()

@app.route('/api/warframes')
def get_warframes():
    db = None
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        db = get_db()
        query = db.query(Warframe)
        if search:
            search = f"%{search}%"
            query = query.filter(Warframe.name_en.ilike(search))
        
        total = query.count()
        warframes = query.offset((page - 1) * per_page).limit(per_page).all()
        
        response = jsonify({
            'success': True,
            'data': [{
                'id': str(w.id),
                'name_en': w.name_en,
                'name_zh': w.name_zh,
                'name_alias': w.name_alias,
                'description_en': w.description_en,
                'description_zh': w.description_zh,
                'health': w.health,
                'shield': w.shield,
                'armor': w.armor,
                'energy': w.energy,
                'sprint_speed': w.sprint_speed,
                'mastery_rank': w.mastery_rank,
                'abilities_en': w.abilities_en,
                'abilities_zh': w.abilities_zh,
                'passive_en': w.passive_en,
                'passive_zh': w.passive_zh,
                'polarities': w.polarities,
                'last_updated': w.last_updated.strftime('%Y-%m-%d %H:%M:%S') if w.last_updated else None
            } for w in warframes],
            'total': total,
            'page': page,
            'per_page': per_page
        })
        return no_cache_response(response)
    except Exception as e:
        app.logger.error(f"获取Warframes数据失败: {str(e)}")
        if db:
            db.rollback()
        response = jsonify({'success': False, 'error': str(e)})
        return no_cache_response(response)
    finally:
        if db:
            db.close()

@app.route('/api/weapons')
def get_weapons():
    db = None
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        db = get_db()
        query = db.query(Weapon)
        if search:
            search = f"%{search}%"
            query = query.filter(Weapon.name_en.ilike(search))
        
        total = query.count()
        weapons = query.offset((page - 1) * per_page).limit(per_page).all()
        
        response = jsonify({
            'success': True,
            'data': [{
                'id': str(w.id),
                'name_en': w.name_en,
                'name_zh': w.name_zh,
                'name_alias': w.name_alias,
                'description_en': w.description_en,
                'description_zh': w.description_zh,
                'type': w.type,
                'mastery_rank': w.mastery_rank,
                'damage': w.damage,
                'critical_chance': w.critical_chance,
                'critical_multiplier': w.critical_multiplier,
                'status_chance': w.status_chance,
                'fire_rate': w.fire_rate,
                'accuracy': w.accuracy,
                'magazine_size': w.magazine_size,
                'reload_time': w.reload_time,
                'disposition': w.disposition,
                'last_updated': w.last_updated.strftime('%Y-%m-%d %H:%M:%S') if w.last_updated else None
            } for w in weapons],
            'total': total,
            'page': page,
            'per_page': per_page
        })
        return no_cache_response(response)
    except Exception as e:
        app.logger.error(f"获取Weapons数据失败: {str(e)}")
        if db:
            db.rollback()
        response = jsonify({'success': False, 'error': str(e)})
        return no_cache_response(response)
    finally:
        if db:
            db.close()

@app.route('/api/mods')
def get_mods():
    db = None
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', '')
        
        db = get_db()
        query = db.query(Mod)
        if search:
            search = f"%{search}%"
            query = query.filter(Mod.name_en.ilike(search))
        
        total = query.count()
        mods = query.offset((page - 1) * per_page).limit(per_page).all()
        
        response = jsonify({
            'success': True,
            'data': [{
                'id': str(m.id),
                'name_en': m.name_en,
                'name_zh': m.name_zh,
                'name_alias': m.name_alias,
                'description_en': m.description_en,
                'description_zh': m.description_zh,
                'polarity': m.polarity,
                'rarity': m.rarity,
                'drain': m.drain,
                'effect_en': m.effect_en,
                'effect_zh': m.effect_zh,
                'max_rank': m.max_rank,
                'tradable': m.tradable,
                'mod_set': m.mod_set,
                'base_effects': m.base_effects,
                'upgrade_effects': m.upgrade_effects,
                'last_updated': m.last_updated.strftime('%Y-%m-%d %H:%M:%S') if m.last_updated else None
            } for m in mods],
            'total': total,
            'page': page,
            'per_page': per_page
        })
        return no_cache_response(response)
    except Exception as e:
        app.logger.error(f"获取Mods数据失败: {str(e)}")
        if db:
            db.rollback()
        response = jsonify({'success': False, 'error': str(e)})
        return no_cache_response(response)
    finally:
        if db:
            db.close()

@app.route('/api/<string:data_type>/<path:item_id>', methods=['PUT'])
def update_item(data_type, item_id):
    db = None
    try:
        app.logger.info(f"收到更新请求 - 类型: {data_type}, ID: {item_id}")
        app.logger.info(f"请求数据: {request.get_json()}")
        
        data = request.get_json()
        if not data:
            app.logger.error("无效的请求数据")
            return jsonify({'success': False, 'error': '无效的请求数据'})

        # 验证数据类型
        if data_type not in ['warframes', 'weapons', 'mods']:
            app.logger.error(f"无效的数据类型: {data_type}")
            return jsonify({'success': False, 'error': '无效的数据类型'})

        db = get_db()
        # 根据数据类型获取对应的模型
        model_map = {
            'warframes': Warframe,
            'weapons': Weapon,
            'mods': Mod
        }
        model = model_map[data_type]

        # 查找要更新的记录
        normalized_id = '/' + item_id if not item_id.startswith('/') else item_id
        app.logger.info(f"查询ID: {normalized_id}")
        item = db.query(model).filter(model.id == normalized_id).first()
        if not item:
            app.logger.error(f"未找到记录 - 类型: {data_type}, ID: {normalized_id}")
            return jsonify({'success': False, 'error': '未找到要更新的项目'})

        # 更新记录
        for key, value in data.items():
            if key != 'id' and key != 'last_updated' and hasattr(item, key):
                if key == 'damage' and isinstance(value, dict):
                    value = json.dumps(value)
                setattr(item, key, value)
        
        item.last_updated = datetime.utcnow()
        
        try:
            db.commit()
            app.logger.info("更新成功")
            
            # 转换为字典
            result = {
                'id': str(item.id),
                'name_en': item.name_en,
                'name_zh': item.name_zh,
                'name_alias': item.name_alias,
                'last_updated': item.last_updated.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # 根据数据类型添加特定字段
            if data_type == 'warframes':
                result.update({
                    'health': item.health,
                    'shield': item.shield,
                    'armor': item.armor,
                    'energy': item.energy,
                    'sprint_speed': item.sprint_speed,
                    'mastery_rank': item.mastery_rank,
                    'description_en': item.description_en,
                    'description_zh': item.description_zh,
                    'abilities_en': item.abilities_en,
                    'abilities_zh': item.abilities_zh,
                    'passive_en': item.passive_en,
                    'passive_zh': item.passive_zh,
                    'polarities': item.polarities
                })
            elif data_type == 'weapons':
                result.update({
                    'type': item.type,
                    'mastery_rank': item.mastery_rank,
                    'damage': item.damage,
                    'critical_chance': item.critical_chance,
                    'critical_multiplier': item.critical_multiplier,
                    'status_chance': item.status_chance,
                    'fire_rate': item.fire_rate,
                    'accuracy': item.accuracy,
                    'magazine_size': item.magazine_size,
                    'reload_time': item.reload_time,
                    'disposition': item.disposition,
                    'description_en': item.description_en,
                    'description_zh': item.description_zh
                })
            elif data_type == 'mods':
                result.update({
                    'polarity': item.polarity,
                    'rarity': item.rarity,
                    'drain': item.drain,
                    'max_rank': item.max_rank,
                    'tradable': item.tradable,
                    'mod_set': item.mod_set,
                    'effect_en': item.effect_en,
                    'effect_zh': item.effect_zh,
                    'base_effects': item.base_effects,
                    'upgrade_effects': item.upgrade_effects,
                    'description_en': item.description_en,
                    'description_zh': item.description_zh
                })
            
            response = jsonify({
                'success': True,
                'data': result
            })
            return no_cache_response(response)
            
        except Exception as e:
            db.rollback()
            app.logger.error(f"数据库更新失败: {str(e)}")
            return jsonify({'success': False, 'error': f'更新失败: {str(e)}'})

    except Exception as e:
        app.logger.error(f"处理更新请求失败: {str(e)}")
        if db:
            db.rollback()
        return jsonify({'success': False, 'error': f'处理请求失败: {str(e)}'})
    finally:
        if db:
            db.close()

def run_crawler_task(spider_type=None):
    """在单独的进程中运行爬虫
    Args:
        spider_type: 可选值为 'warframes', 'weapons', 'mods' 或 None（爬取所有）
    """
    try:
        # 创建自定义设置
        settings = get_project_settings()
        settings.set('LOG_ENABLED', True)
        settings.set('LOG_LEVEL', 'INFO')
        
        # 初始化爬虫进程
        process = CrawlerProcess(settings)
        
        # 根据类型选择要运行的爬虫
        if spider_type == 'warframes':
            process.crawl(WarframeSpider)
            print(f'正在运行Warframe爬虫...')
        elif spider_type == 'weapons':
            process.crawl(WeaponSpider)
            print(f'正在运行Weapon爬虫...')
        elif spider_type == 'mods':
            process.crawl(ModSpider)
            print(f'正在运行Mod爬虫...')
        else:
            # 运行所有爬虫
            print(f'正在运行所有爬虫...')
            process.crawl(WarframeSpider)
            process.crawl(WeaponSpider)
            process.crawl(ModSpider)
        
        # 启动爬虫进程
        process.start(stop_after_crawl=True)
        
    except Exception as e:
        print(f'爬虫进程出错: {str(e)}')

def update_crawler_status(new_status):
    """更新爬虫状态"""
    global crawler_status
    crawler_status.update(new_status)

@app.route('/api/crawler/status')
def get_crawler_status():
    return jsonify(crawler_status)

@app.route('/api/crawler/start', methods=['POST'])
def start_crawler():
    global crawler_status
    
    if crawler_status['is_running']:
        return jsonify({
            'success': False,
            'message': '爬虫任务已在运行中'
        })
    
    try:
        # 获取要爬取的数据类型
        spider_type = request.json.get('type') if request.json else None
        
        # 更新状态消息
        status_message = '爬虫任务正在运行...'
        if spider_type:
            status_message = f'正在更新{spider_type}数据...'
        
        # 更新状态为运行中
        update_crawler_status({
            'is_running': True,
            'message': status_message,
            'last_run': time.strftime('%Y-%m-%d %H:%M:%S'),
            'current_type': spider_type or 'all'
        })
        
        # 创建新进程运行爬虫
        crawler_process = multiprocessing.Process(
            target=run_crawler_task,
            args=(spider_type,)
        )
        crawler_process.start()
        
        # 启动监控进程状态的线程
        def monitor_crawler():
            while crawler_process.is_alive():
                time.sleep(1)
            
            # 爬虫进程结束后更新状态
            completion_message = '爬虫任务完成'
            if spider_type:
                completion_message = f'{spider_type}数据更新完成'
            
            update_crawler_status({
                'is_running': False,
                'message': completion_message,
                'last_run': time.strftime('%Y-%m-%d %H:%M:%S'),
                'current_type': None
            })
        
        import threading
        monitor_thread = threading.Thread(target=monitor_crawler)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        return jsonify({
            'success': True,
            'message': '爬虫任务已启动'
        })
        
    except Exception as e:
        error_msg = f'启动爬虫失败: {str(e)}'
        app.logger.error(error_msg)
        update_crawler_status({
            'is_running': False,
            'message': error_msg,
        })
        return jsonify({
            'success': False,
            'message': error_msg
        })

def run_web_interface(host, port):
    """启动Web界面"""
    app.logger.setLevel(logging.INFO)
    # 禁用reloader以避免Windows下的套接字问题
    app.run(host=host, port=port, debug=True, use_reloader=False) 