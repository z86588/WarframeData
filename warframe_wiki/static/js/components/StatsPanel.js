const StatsPanel = {
    data() {
        return {
            stats: {
                warframes: {
                    count: 0,
                    last_updated: null
                },
                weapons: {
                    count: 0,
                    last_updated: null
                },
                mods: {
                    count: 0,
                    last_updated: null
                }
            },
            error: null,
            loading: false
        };
    },
    template: `
        <div class="stats-card card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h6 class="mb-0">数据统计</h6>
            </div>
            <div class="card-body">
                <div class="row g-3">
                    <div class="col-md-4">
                        <div class="stat-item">
                            <div class="stat-content">
                                <div class="stat-header">
                                    <span class="stat-label">Warframes</span>
                                    <span class="stat-value">{{ stats.warframes.count }}</span>
                                </div>
                                <div class="stat-footer">
                                    <small class="text-muted">最后更新: {{ formatDate(stats.warframes.last_updated) }}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="stat-item">
                            <div class="stat-content">
                                <div class="stat-header">
                                    <span class="stat-label">Weapons</span>
                                    <span class="stat-value">{{ stats.weapons.count }}</span>
                                </div>
                                <div class="stat-footer">
                                    <small class="text-muted">最后更新: {{ formatDate(stats.weapons.last_updated) }}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="stat-item">
                            <div class="stat-content">
                                <div class="stat-header">
                                    <span class="stat-label">Mods</span>
                                    <span class="stat-value">{{ stats.mods.count }}</span>
                                </div>
                                <div class="stat-footer">
                                    <small class="text-muted">最后更新: {{ formatDate(stats.mods.last_updated) }}</small>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-if="error" class="alert alert-danger mt-3">
                    {{ error }}
                </div>
            </div>
        </div>
    `,
    methods: {
        formatDate(dateStr) {
            if (!dateStr) return '暂无数据';
            const date = new Date(dateStr);
            return date.toLocaleString();
        },
        async fetchStats() {
            if (this.loading) return;
            
            this.loading = true;
            
            try {
                const response = await fetch('/api/stats');
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const result = await response.json();
                
                if (!result.success) {
                    throw new Error(result.error || '获取统计数据失败');
                }
                
                this.stats = {
                    warframes: result.data.warframes || { count: 0, last_updated: null },
                    weapons: result.data.weapons || { count: 0, last_updated: null },
                    mods: result.data.mods || { count: 0, last_updated: null }
                };
                
                this.error = null;
            } catch (e) {
                this.error = `获取统计数据失败: ${e.message}`;
            } finally {
                this.loading = false;
            }
        }
    },
    mounted() {
        this.fetchStats();
    }
}; 