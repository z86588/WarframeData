const DataTable = {
    props: {
        type: {
            type: String,
            required: true
        },
        columns: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            items: [],
            loading: false,
            error: null,
            searchQuery: '',
            pagination: {
                total: 0,
                page: 1,
                perPage: 10
            }
        };
    },
    template: `
        <div class="table-container">
            <!-- 搜索框 -->
            <div class="vgt-global-search mb-3">
                <input type="text" class="form-control" 
                       placeholder="搜索..." 
                       v-model="searchQuery"
                       @input="onSearch">
            </div>

            <!-- 数据表格 -->
            <div class="table-content">
                <div v-if="loading" class="loading-overlay">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">加载中...</span>
                    </div>
                </div>
                
                <table class="vgt-table">
                    <thead>
                        <tr>
                            <th v-for="col in columns" :key="col.field" :data-field="col.field" :style="getColumnStyle(col)">
                                {{ col.label }}
                            </th>
                            <th class="action-column">操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="item in items" :key="item.id">
                            <td v-for="col in columns" :key="col.field" :data-field="col.field" :style="getColumnStyle(col)">
                                <template v-if="col.template">
                                    <div v-html="col.template(item)"></div>
                                </template>
                                <template v-else-if="col.type === 'number'">
                                    <span class="number-cell">{{ item[col.field] }}</span>
                                </template>
                                <template v-else-if="col.type === 'boolean'">
                                    {{ item[col.field] ? '是' : '否' }}
                                </template>
                                <template v-else>
                                    {{ item[col.field] }}
                                </template>
                            </td>
                            <td class="action-column">
                                <button class="btn btn-sm btn-outline-primary" @click="editItem(item)">
                                    编辑
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- 分页 -->
            <div v-if="!loading && items.length > 0" class="pagination-container">
                <nav aria-label="Page navigation">
                    <ul class="pagination justify-content-center mb-0">
                        <li class="page-item" :class="{ disabled: pagination.page === 1 }">
                            <a class="page-link" href="#" @click.prevent="changePage(pagination.page - 1)">
                                上一页
                            </a>
                        </li>
                        <li v-for="pageNum in pageNumbers" 
                            :key="pageNum" 
                            class="page-item"
                            :class="{ active: pageNum === pagination.page }">
                            <a class="page-link" href="#" @click.prevent="changePage(pageNum)">
                                {{ pageNum }}
                            </a>
                        </li>
                        <li class="page-item" :class="{ disabled: pagination.page === totalPages }">
                            <a class="page-link" href="#" @click.prevent="changePage(pagination.page + 1)">
                                下一页
                            </a>
                        </li>
                    </ul>
                </nav>
            </div>
        </div>
    `,
    computed: {
        totalPages() {
            return Math.ceil(this.pagination.total / this.pagination.perPage);
        },
        pageNumbers() {
            const pages = [];
            const maxVisiblePages = 5;
            let start = Math.max(1, this.pagination.page - Math.floor(maxVisiblePages / 2));
            let end = Math.min(this.totalPages, start + maxVisiblePages - 1);
            
            if (end - start + 1 < maxVisiblePages) {
                start = Math.max(1, end - maxVisiblePages + 1);
            }
            
            for (let i = start; i <= end; i++) {
                pages.push(i);
            }
            return pages;
        }
    },
    methods: {
        async fetchData() {
            this.loading = true;
            this.error = null;
            try {
                const params = new URLSearchParams({
                    page: this.pagination.page,
                    per_page: this.pagination.perPage,
                    search: this.searchQuery
                });
                
                const response = await fetch(`/api/${this.type}?${params}`);
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const result = await response.json();
                
                if (!result.success) {
                    throw new Error(result.error || '获取数据失败');
                }
                
                this.items = result.data.map(item => {
                    // 处理极性数据
                    let parsedPolarities = item.polarities;
                    if (typeof item.polarities === 'string') {
                        try {
                            parsedPolarities = JSON.parse(item.polarities);
                        } catch (e) {
                            parsedPolarities = [];
                        }
                    } else if (!Array.isArray(item.polarities)) {
                        parsedPolarities = [];
                    }
                    
                    // 处理技能数据
                    let abilities_en = item.abilities_en;
                    let abilities_zh = item.abilities_zh;
                    
                    // 如果技能数据是字符串，保持原样（让模板处理解析）
                    // 如果已经是对象，转换为字符串
                    if (typeof abilities_en === 'object' && abilities_en !== null) {
                        abilities_en = JSON.stringify(abilities_en);
                    }
                    if (typeof abilities_zh === 'object' && abilities_zh !== null) {
                        abilities_zh = JSON.stringify(abilities_zh);
                    }
                    
                    return {
                        ...item,
                        description_en: this.removeMarkupTags(item.description_en),
                        description_zh: this.removeMarkupTags(item.description_zh),
                        abilities_en,
                        abilities_zh,
                        damage: typeof item.damage === 'object' ? JSON.stringify(item.damage) : item.damage,
                        base_effects: typeof item.base_effects === 'object' ? JSON.stringify(item.base_effects) : item.base_effects,
                        upgrade_effects: typeof item.upgrade_effects === 'object' ? JSON.stringify(item.upgrade_effects) : item.upgrade_effects,
                        polarities: parsedPolarities,
                        passive_en: this.removeMarkupTags(item.passive_en),
                        passive_zh: this.removeMarkupTags(item.passive_zh),
                        effect_en: this.removeMarkupTags(item.effect_en),
                        effect_zh: this.removeMarkupTags(item.effect_zh)
                    };
                });
                
                this.pagination.total = result.total;
                this.pagination.page = result.page;
                this.pagination.perPage = result.per_page;
            } catch (e) {
                this.error = `获取${this.type}数据失败: ${e.message}`;
                console.error(e);
                this.items = [];
            } finally {
                this.loading = false;
            }
        },
        removeMarkupTags(text) {
            if (!text) return '';
            return text.replace(/<[^>]+>/g, '');
        },
        onSearch() {
            this.pagination.page = 1;
            this.fetchData();
        },
        async changePage(newPage) {
            if (newPage < 1 || newPage > this.totalPages || newPage === this.pagination.page) {
                return;
            }
            this.pagination.page = newPage;
            await this.fetchData();
        },
        editItem(item) {
            this.$emit('edit-item', item);
        },
        getColumnStyle(column) {
            // Warframes表格的列宽设置
            const columnWidths = {
                // 名称列 - 增加20px宽度
                'name_en': { width: '140px', minWidth: '140px' },
                'name_zh': { width: '140px', minWidth: '140px' },
                'name_alias': { width: '100px', minWidth: '100px' },
                
                // 数值列 - 由于显示数字，可以较窄
                'health': { width: '70px', minWidth: '70px' },
                'shield': { width: '70px', minWidth: '70px' },
                'armor': { width: '70px', minWidth: '70px' },
                'energy': { width: '70px', minWidth: '70px' },
                'sprint_speed': { width: '80px', minWidth: '80px' },
                
                // 技能列
                'abilities_en': { width: '210px', minWidth: '210px' },
                'abilities_zh': { width: '180px', minWidth: '180px' },
                
                // 被动列 - 增加20px宽度
                'passive_en': { width: '290px', minWidth: '290px' },
                'passive_zh': { width: '290px', minWidth: '290px' },
                
                // 极性列
                'polarities': { width: '80px', minWidth: '80px' }
            };
            
            return columnWidths[column.field] || {};
        }
    },
    watch: {
        type: {
            handler() {
                this.pagination.page = 1;
                this.searchQuery = '';
                this.fetchData();
            },
            immediate: true
        }
    }
}; 