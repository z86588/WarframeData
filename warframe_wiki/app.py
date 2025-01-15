from flask import Flask, request, jsonify
import sqlite3
import json
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

# 确保日志目录存在
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志
log_file = os.path.join(log_dir, 'warframe_wiki.log')
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=3)
handler.setFormatter(logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s'
))
app.logger.addHandler(handler)

def get_db_connection():
    conn = sqlite3.connect('warframe_wiki/warframe.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/<string:data_type>/<path:item_id>', methods=['PUT'])
def update_item(data_type, item_id):
    conn = None
    cursor = None
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

        # 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor()

        # 记录当前ID是否存在
        cursor.execute(f"SELECT COUNT(*) FROM {data_type} WHERE id = ?", (item_id,))
        if cursor.fetchone()[0] == 0:
            app.logger.error(f"未找到记录 - 类型: {data_type}, ID: {item_id}")
            return jsonify({'success': False, 'error': '未找到要更新的项目'})

        # 构建更新语句
        update_fields = []
        params = []
        for key, value in data.items():
            if key != 'id' and key != 'last_updated':
                if key == 'damage' and isinstance(value, dict):
                    value = json.dumps(value)
                update_fields.append(f"{key} = ?")
                params.append(value)
        
        # 添加更新时间
        update_fields.append("last_updated = datetime('now')")
        
        # 添加ID到参数列表
        params.append(item_id)
        
        # 执行更新
        update_sql = f"UPDATE {data_type} SET {', '.join(update_fields)} WHERE id = ?"
        app.logger.info(f"执行SQL: {update_sql}")
        app.logger.info(f"参数: {params}")
        
        cursor.execute(update_sql, params)
        
        # 获取更新后的数据
        cursor.execute(f"SELECT * FROM {data_type} WHERE id = ?", (item_id,))
        updated_item = cursor.fetchone()
        
        if not updated_item:
            app.logger.error("更新后未找到记录")
            conn.rollback()
            return jsonify({'success': False, 'error': '更新失败'})
        
        # 转换为字典
        columns = [desc[0] for desc in cursor.description]
        result = dict(zip(columns, updated_item))
        
        conn.commit()
        app.logger.info("更新成功")
        return jsonify({
            'success': True,
            'data': result
        })

    except sqlite3.Error as e:
        app.logger.error(f"数据库错误: {str(e)}")
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': f'数据库错误: {str(e)}'})
    except Exception as e:
        app.logger.error(f"服务器错误: {str(e)}")
        if conn:
            conn.rollback()
        return jsonify({'success': False, 'error': f'服务器错误: {str(e)}'})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=8080) 