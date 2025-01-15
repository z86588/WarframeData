import json
from datetime import datetime
from .database import init_db, Warframe, Weapon, Mod
from .items import WarframeItem, WeaponItem, ModItem

class WarframeWikiPipeline:
    def __init__(self):
        self.db = init_db()
        self.item_models = {
            WarframeItem: Warframe,
            WeaponItem: Weapon,
            ModItem: Mod
        }

    def process_item(self, item, spider):
        model_class = self.item_models[type(item)]
        
        # 检查记录是否存在
        existing = self.db.query(model_class).filter_by(id=item['id']).first()
        
        if existing:
            # 更新现有记录
            for key, value in dict(item).items():
                if value is not None:  # 只更新非空值
                    setattr(existing, key, value)
            existing.last_updated = datetime.utcnow()
        else:
            # 创建新记录
            db_item = model_class(**dict(item))
            self.db.add(db_item)

        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

        return item

    def close_spider(self, spider):
        self.db.close()

    def export_to_json(self, file_path):
        """导出数据为JSON格式"""
        data = {}
        for item_class, model_class in self.item_models.items():
            items = self.db.query(model_class).all()
            data[model_class.__tablename__] = [
                {c.name: getattr(item, c.name) 
                 for c in item.__table__.columns}
                for item in items
            ]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    def export_to_csv(self, directory):
        """导出数据为CSV格式，每种类型一个文件"""
        import pandas as pd
        import os
        
        os.makedirs(directory, exist_ok=True)
        
        for item_class, model_class in self.item_models.items():
            items = self.db.query(model_class).all()
            data = [
                {c.name: getattr(item, c.name) 
                 for c in item.__table__.columns}
                for item in items
            ]
            
            if data:
                df = pd.DataFrame(data)
                file_path = os.path.join(directory, f"{model_class.__tablename__}.csv")
                df.to_csv(file_path, index=False, encoding='utf-8') 