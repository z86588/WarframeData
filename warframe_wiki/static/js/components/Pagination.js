const Pagination = {
    props: {
        currentPage: {
            type: Number,
            required: true
        },
        totalPages: {
            type: Number,
            required: true
        },
        total: {
            type: Number,
            required: true
        },
        perPage: {
            type: Number,
            required: true
        }
    },
    computed: {
        pageNumbers() {
            const pages = [];
            const maxVisiblePages = 5;
            let start = Math.max(1, this.currentPage - Math.floor(maxVisiblePages / 2));
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
    template: `
        <div class="pagination-container">
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    共 {{ total }} 条记录，每页 {{ perPage }} 条
                </div>
                <nav aria-label="Page navigation">
                    <ul class="pagination mb-0">
                        <li class="page-item" :class="{ disabled: currentPage === 1 }">
                            <a class="page-link" href="#" @click.prevent="$emit('change-page', currentPage - 1)" aria-label="Previous">
                                <span aria-hidden="true">&laquo;</span>
                            </a>
                        </li>
                        <li class="page-item" v-for="p in pageNumbers" :key="p" :class="{ active: currentPage === p }">
                            <a class="page-link" href="#" @click.prevent="$emit('change-page', p)">{{ p }}</a>
                        </li>
                        <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                            <a class="page-link" href="#" @click.prevent="$emit('change-page', currentPage + 1)" aria-label="Next">
                                <span aria-hidden="true">&raquo;</span>
                            </a>
                        </li>
                    </ul>
                </nav>
            </div>
        </div>
    `
}; 