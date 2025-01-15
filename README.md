# Warframe Wiki 数据管理系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python](https://img.shields.io/badge/python-3.9-blue.svg)
![Vue.js](https://img.shields.io/badge/vue.js-2.x-green.svg)
![Bootstrap](https://img.shields.io/badge/bootstrap-5.x-purple.svg)

这是一个用于管理 Warframe 游戏数据的 Web 应用系统。该系统提供了战甲、武器和 Mod 的数据管理功能，支持数据的展示、搜索、编辑和爬取。

## 功能特性

### 1. 数据展示
- 支持战甲(Warframes)、武器(Weapons)和 Mod 三种数据类型的展示
- 表格化展示，支持自适应列宽
- 中英文数据对照显示
- 行交替背景色，提升可读性
- 鼠标悬停效果增强

### 2. 数据管理
- 支持按类型搜索数据
- 分页显示，优化大量数据的加载
- 支持数据编辑功能
- 编辑界面支持 JSON 数据的格式化展示

### 3. 数据爬取
- 支持全量数据爬取
- 支持按类型（战甲/武器/Mod）爬取
- 实时显示爬取状态
- 自动更新数据统计

### 4. 界面特性
- 响应式设计，支持不同屏幕尺寸
- 信息图标提示功能
- 数据编辑模态框
- 加载状态提示

## 技术栈

- 前端框架：Vue.js
- UI 组件：Bootstrap
- 图标库：Font Awesome
- 后端：Python Flask
- 数据库：SQLite

## 目录结构

```
warframe_wiki/
├── static/
│   ├── css/
│   │   └── table.css          # 表格样式
│   ├── js/
│   │   ├── components/        # Vue组件
│   │   │   ├── DataTable.js   # 数据表格组件
│   │   │   ├── EditModal.js   # 编辑模态框组件
│   │   │   └── CrawlerControl.js # 爬虫控制组件
│   │   └── columns.js         # 列配置
│   └── index.html             # 主页面
└── app.py                     # 后端应用
```

## 使用说明

1. 数据浏览
   - 点击顶部导航栏选择数据类型（战甲/武器/Mod）
   - 使用搜索框进行数据过滤
   - 点击分页按钮浏览更多数据

2. 数据编辑
   - 点击每行末尾的"编辑"按钮打开编辑界面
   - 修改数据后点击"保存"按钮提交更改

3. 数据爬取
   - 使用顶部的爬虫控制面板
   - 可选择全量爬取或按类型爬取
   - 等待爬取完成后自动刷新数据

## 开发说明

1. 克隆项目
```bash
git clone [repository-url]
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行项目
```bash
python app.py
```

## 注意事项

- 首次运行需要先爬取数据
- 编辑数据时注意保持 JSON 格式的正确性
- 建议定期备份数据库

## 后续计划

- [ ] 添加数据导出功能
- [ ] 优化爬虫性能
- [ ] 添加数据变更日志
- [ ] 增加用户权限管理 

## 许可证

本项目采用 MIT 许可证。查看 [LICENSE](LICENSE) 文件了解更多信息。

## 贡献

欢迎提交问题和改进建议！如果您想为项目做出贡献：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 联系方式

项目维护者：z86588
项目链接：[https://github.com/z86588/WarframeData](https://github.com/z86588/WarframeData) 