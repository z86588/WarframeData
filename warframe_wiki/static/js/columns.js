const warframeColumns = [
    { 
        field: 'name_en', 
        label: '英文名称',
        template: (item) => `${item.name_en} <i class="fas fa-info-circle info-icon" data-type="en" data-id="${item.id}"></i>`
    },
    { 
        field: 'name_zh', 
        label: '中文名称',
        template: (item) => `${item.name_zh} <i class="fas fa-info-circle info-icon" data-type="zh" data-id="${item.id}"></i>`
    },
    { field: 'name_alias', label: '别名' },
    { 
        field: 'health', 
        label: '生命值', 
        type: 'number',
        template: (item) => `<span class="number-cell">${Number(item.health).toFixed(0)}</span>`
    },
    { 
        field: 'shield', 
        label: '护盾值', 
        type: 'number',
        template: (item) => `<span class="number-cell">${Number(item.shield).toFixed(0)}</span>`
    },
    { 
        field: 'armor', 
        label: '护甲值', 
        type: 'number',
        template: (item) => `<span class="number-cell">${Number(item.armor).toFixed(0)}</span>`
    },
    { 
        field: 'energy', 
        label: '能量值', 
        type: 'number',
        template: (item) => `<span class="number-cell">${Number(item.energy).toFixed(0)}</span>`
    },
    { 
        field: 'sprint_speed', 
        label: '移动速度', 
        type: 'number',
        template: (item) => `<span class="number-cell">${item.sprint_speed}</span>`
    },
    { 
        field: 'abilities_en', 
        label: '英文技能',
        template: (item) => {
            try {
                const abilities = JSON.parse(item.abilities_en || '[]');
                return abilities.map((ability, index) => 
                    `<div class="ability-item">
                        ${ability.name}
                        <i class="fas fa-info-circle info-icon" 
                           data-type="ability-en" 
                           data-id="${item.id}" 
                           data-index="${index}"></i>
                    </div>`
                ).join('');
            } catch (e) {
                console.error('解析英文技能数据失败:', e, item.abilities_en);
                return '';
            }
        }
    },
    { 
        field: 'abilities_zh', 
        label: '中文技能',
        template: (item) => {
            try {
                const abilities = JSON.parse(item.abilities_zh || '[]');
                return abilities.map((ability, index) => 
                    `<div class="ability-item">
                        ${ability.name}
                        <i class="fas fa-info-circle info-icon" 
                           data-type="ability-zh" 
                           data-id="${item.id}" 
                           data-index="${index}"></i>
                    </div>`
                ).join('');
            } catch (e) {
                console.error('解析中文技能数据失败:', e, item.abilities_zh);
                return '';
            }
        }
    },
    { field: 'passive_en', label: '英文被动' },
    { field: 'passive_zh', label: '中文被动' },
    { 
        field: 'polarities', 
        label: '极性',
        template: (item) => {
            try {
                const polarities = Array.isArray(item.polarities) ? 
                    item.polarities : 
                    JSON.parse(item.polarities || '[]');
                    
                if (!polarities || !polarities.length) return '无';
                
                return `<div class="polarities-container">
                    ${polarities.map(polarity => 
                        `<span class="polarity-tag">
                            ${polarity}
                        </span>`
                    ).join('')}
                </div>`;
            } catch (e) {
                console.error('解析极性数据失败:', e, item.polarities);
                return '无';
            }
        }
    }
];

const weaponColumns = [
    { 
        field: 'name_en', 
        label: '英文名称',
        template: (item) => `${item.name_en} <i class="fas fa-info-circle info-icon" data-type="en" data-id="${item.id}"></i>`
    },
    { 
        field: 'name_zh', 
        label: '中文名称',
        template: (item) => `${item.name_zh} <i class="fas fa-info-circle info-icon" data-type="zh" data-id="${item.id}"></i>`
    },
    { field: 'name_alias', label: '别名' },
    { field: 'type', label: '类型' },
    { field: 'mastery_rank', label: '段位', type: 'number' },
    { field: 'damage', label: '伤害', type: 'json' },
    { field: 'critical_chance', label: '暴击率', type: 'number' },
    { field: 'critical_multiplier', label: '暴击倍率', type: 'number' },
    { field: 'status_chance', label: '触发率', type: 'number' },
    { field: 'fire_rate', label: '射速', type: 'number' },
    { field: 'accuracy', label: '精准度', type: 'number' },
    { field: 'magazine_size', label: '弹匣容量', type: 'number' },
    { field: 'reload_time', label: '装填时间', type: 'number' },
    { field: 'disposition', label: '裂罅倾向', type: 'number' }
];

const modColumns = [
    { 
        field: 'name_en', 
        label: '英文名称',
        template: (item) => `${item.name_en} <i class="fas fa-info-circle info-icon" data-type="en" data-id="${item.id}"></i>`
    },
    { 
        field: 'name_zh', 
        label: '中文名称',
        template: (item) => `${item.name_zh} <i class="fas fa-info-circle info-icon" data-type="zh" data-id="${item.id}"></i>`
    },
    { field: 'name_alias', label: '别名' },
    { field: 'polarity', label: '极性' },
    { field: 'rarity', label: '稀有度' },
    { field: 'drain', label: '消耗', type: 'number' },
    { field: 'max_rank', label: '最大等级', type: 'number' },
    { field: 'effect_en', label: '英文效果' },
    { field: 'effect_zh', label: '中文效果' },
    { field: 'tradable', label: '可交易', type: 'boolean' },
    { field: 'mod_set', label: '套装' },
    { field: 'base_effects', label: '基础效果', type: 'json' },
    { field: 'upgrade_effects', label: '升级效果', type: 'json' }
]; 