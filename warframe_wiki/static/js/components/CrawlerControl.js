const CrawlerControl = {
    props: {
        crawlerStatus: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            statusCheckInterval: null,
            error: null
        };
    },
    template: `
        <div class="crawler-control">
            <div class="card h-100">
                <div class="card-header d-flex justify-content-between align-items-center">
                    <h6 class="mb-0">爬虫控制</h6>
                    <span class="badge" :class="statusBadgeClass">
                        {{ crawlerStatus.is_running ? '运行中' : '空闲' }}
                    </span>
                </div>
                <div class="card-body">
                    <div class="status-info mb-3">
                        <div v-if="crawlerStatus.current_type" class="status-item">
                            <i class="fas fa-tasks"></i>
                            <span>当前任务: {{ crawlerStatus.current_type }}</span>
                        </div>
                        <div v-if="crawlerStatus.message" class="status-item">
                            <i class="fas fa-info-circle"></i>
                            <span>{{ crawlerStatus.message }}</span>
                        </div>
                        <div v-if="crawlerStatus.last_run" class="status-item">
                            <i class="fas fa-clock"></i>
                            <span>上次运行: {{ new Date(crawlerStatus.last_run).toLocaleString() }}</span>
                        </div>
                    </div>
                    
                    <div class="crawler-actions">
                        <button class="btn btn-primary w-100 mb-3" 
                                @click="startCrawler()"
                                :disabled="crawlerStatus.is_running">
                            <i class="fas fa-sync-alt"></i> 爬取全部分类
                        </button>
                        
                        <div class="row g-2">
                            <div class="col-md-4">
                                <button class="btn btn-outline-primary w-100" 
                                        @click="startCrawler('warframes')"
                                        :disabled="crawlerStatus.is_running">
                                    <i class="fas fa-robot"></i>
                                    <span class="d-block">Warframes爬取</span>
                                </button>
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-outline-primary w-100" 
                                        @click="startCrawler('weapons')"
                                        :disabled="crawlerStatus.is_running">
                                    <i class="fas fa-crosshairs"></i>
                                    <span class="d-block">Weapons爬取</span>
                                </button>
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-outline-primary w-100" 
                                        @click="startCrawler('mods')"
                                        :disabled="crawlerStatus.is_running">
                                    <i class="fas fa-puzzle-piece"></i>
                                    <span class="d-block">Mods爬取</span>
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <div v-if="error" class="alert alert-danger mt-3">
                        {{ error }}
                    </div>
                </div>
            </div>
        </div>
    `,
    computed: {
        statusBadgeClass() {
            return {
                'badge-success bg-success': !this.crawlerStatus.is_running,
                'badge-warning bg-warning': this.crawlerStatus.is_running
            };
        }
    },
    methods: {
        async startCrawler(type = null) {
            try {
                const response = await fetch('/api/crawler/start', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ type })
                });
                
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const result = await response.json();
                
                if (result.success) {
                    this.$emit('update:crawlerStatus', {
                        ...this.crawlerStatus,
                        is_running: true,
                        current_type: type || 'all'
                    });
                    this.startStatusCheck();
                }
            } catch (e) {
                this.error = `启动爬虫失败: ${e.message}`;
            }
        },
        async checkCrawlerStatus() {
            try {
                const response = await fetch('/api/crawler/status');
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                const newStatus = await response.json();
                
                this.$emit('update:crawlerStatus', {
                    ...newStatus,
                    current_type: newStatus.current_type || this.crawlerStatus.current_type
                });

                if (!newStatus.is_running) {
                    this.stopStatusCheck();
                    this.$emit('crawler-complete');
                }
            } catch (e) {
                // 静默处理状态检查错误
            }
        },
        startStatusCheck() {
            if (this.statusCheckInterval) {
                clearInterval(this.statusCheckInterval);
            }
            this.statusCheckInterval = setInterval(() => {
                this.checkCrawlerStatus();
            }, 2000);
        },
        stopStatusCheck() {
            if (this.statusCheckInterval) {
                clearInterval(this.statusCheckInterval);
                this.statusCheckInterval = null;
            }
        }
    },
    mounted() {
        this.checkCrawlerStatus();
        setInterval(() => {
            this.checkCrawlerStatus();
        }, 30000);
    },
    beforeDestroy() {
        this.stopStatusCheck();
    }
}; 