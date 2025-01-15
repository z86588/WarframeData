const DescriptionTooltip = {
    props: {
        activeDescription: {
            type: Object,
            default: null
        }
    },
    template: `
        <div class="description-tooltip" :class="{ 'show': tooltipVisible }" ref="tooltip" :style="tooltipStyle">
            <template v-if="activeDescription">
                <h6>{{ activeDescription.title }}</h6>
                <p>{{ activeDescription.content }}</p>
            </template>
        </div>
    `,
    data() {
        return {
            tooltipVisible: false,
            tooltipStyle: {
                position: 'fixed',
                zIndex: 9999,
                left: '0px',
                top: '0px'
            }
        };
    },
    methods: {
        removeMarkupTags(text) {
            if (!text) return '';
            return text.replace(/<[^>]+>/g, '');
        },
        showDescription(event, item, type) {
            let title, content;
            
            if (type === 'en' || type === 'zh') {
                title = type === 'en' ? 'English Description' : '中文描述';
                content = type === 'en' ? this.removeMarkupTags(item.description_en) : this.removeMarkupTags(item.description_zh);
            } else if (type === 'ability-en' || type === 'ability-zh') {
                const index = event.target.dataset.index;
                try {
                    const abilities = JSON.parse(type === 'ability-en' ? item.abilities_en : item.abilities_zh);
                    const ability = abilities[index];
                    title = type === 'ability-en' ? 'Ability Description' : '技能描述';
                    content = this.removeMarkupTags(ability.description);
                } catch (e) {
                    return;
                }
            }
            
            if (!content) return;
            
            this.activeDescription = { title, content };
            
            this.$nextTick(() => {
                const iconRect = event.target.getBoundingClientRect();
                const tooltipWidth = 320;
                const padding = 10;
                
                let left = iconRect.right + padding;
                if (left + tooltipWidth > window.innerWidth) {
                    left = iconRect.left - tooltipWidth - padding;
                }
                
                let top = iconRect.top;
                const tooltip = this.$refs.tooltip;
                if (tooltip) {
                    const tooltipHeight = tooltip.offsetHeight;
                    if (top + tooltipHeight > window.innerHeight) {
                        top = window.innerHeight - tooltipHeight - padding;
                    }
                }
                
                this.tooltipStyle = {
                    ...this.tooltipStyle,
                    left: `${left}px`,
                    top: `${top}px`
                };
                
                this.tooltipVisible = true;
            });
        },
        hideDescription() {
            this.tooltipVisible = false;
            
            setTimeout(() => {
                if (!this.tooltipVisible) {
                    this.$emit('update:activeDescription', null);
                }
            }, 200);
        },
        registerEvents() {
            const events = {
                showDescription: this.showDescription.bind(this),
                hideDescription: this.hideDescription.bind(this)
            };
            this.$emit('register-events', events);
            return events;
        }
    },
    mounted() {
        this.$nextTick(() => {
            const events = this.registerEvents();
            this._events = events;
        });
    },
    beforeDestroy() {
        if (this._events) {
            this.$emit('register-events', null);
            this._events = null;
        }
    }
}; 