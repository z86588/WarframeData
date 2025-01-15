const EditModal = {
    props: {
        item: {
            type: Object,
            required: true
        },
        type: {
            type: String,
            required: true
        },
        show: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            editData: {}
        };
    },
    template: `
        <div v-if="show" class="edit-modal">
            <div class="edit-modal-content">
                <h3 class="mb-4">编辑 {{ type }}</h3>
                <form @submit.prevent="save">
                    <!-- 基础信息 -->
                    <div class="form-row">
                        <div class="form-col">
                            <label>英文名称</label>
                            <input type="text" class="form-control" v-model="editData.name_en">
                        </div>
                        <div class="form-col">
                            <label>中文名称</label>
                            <input type="text" class="form-control" v-model="editData.name_zh">
                        </div>
                        <div class="form-col">
                            <label>别名</label>
                            <input type="text" class="form-control" v-model="editData.name_alias">
                        </div>
                    </div>

                    <!-- Warframe特有字段 -->
                    <template v-if="type === 'warframes'">
                        <div class="form-row">
                            <div class="form-col">
                                <label>生命值</label>
                                <input type="number" class="form-control number-input" 
                                       v-model.number="editData.health" 
                                       step="1">
                            </div>
                            <div class="form-col">
                                <label>护盾值</label>
                                <input type="number" class="form-control number-input" 
                                       v-model.number="editData.shield" 
                                       step="1">
                            </div>
                            <div class="form-col">
                                <label>护甲值</label>
                                <input type="number" class="form-control number-input" 
                                       v-model.number="editData.armor" 
                                       step="1">
                            </div>
                            <div class="form-col">
                                <label>能量值</label>
                                <input type="number" class="form-control number-input" 
                                       v-model.number="editData.energy" 
                                       step="1">
                            </div>
                            <div class="form-col">
                                <label>移动速度</label>
                                <input type="number" class="form-control number-input" 
                                       v-model.number="editData.sprint_speed" 
                                       step="any"
                                       min="0">
                            </div>
                        </div>
                    </template>

                    <!-- Weapon特有字段 -->
                    <template v-if="type === 'weapons'">
                        <div class="form-row">
                            <div class="form-col">
                                <label>类型</label>
                                <input type="text" class="form-control" v-model="editData.type">
                            </div>
                            <div class="form-col">
                                <label>段位</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.mastery_rank">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-col">
                                <label>暴击率</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.critical_chance" step="0.1">
                            </div>
                            <div class="form-col">
                                <label>暴击倍率</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.critical_multiplier" step="0.1">
                            </div>
                            <div class="form-col">
                                <label>触发率</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.status_chance" step="0.1">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-col">
                                <label>射速</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.fire_rate" step="0.1">
                            </div>
                            <div class="form-col">
                                <label>精准度</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.accuracy" step="0.1">
                            </div>
                            <div class="form-col">
                                <label>弹匣容量</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.magazine_size">
                            </div>
                            <div class="form-col">
                                <label>装填时间</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.reload_time" step="0.1">
                            </div>
                            <div class="form-col">
                                <label>裂罅倾向</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.disposition">
                            </div>
                        </div>
                    </template>

                    <!-- Mod特有字段 -->
                    <template v-if="type === 'mods'">
                        <div class="form-row">
                            <div class="form-col">
                                <label>极性</label>
                                <input type="text" class="form-control" v-model="editData.polarity">
                            </div>
                            <div class="form-col">
                                <label>稀有度</label>
                                <input type="text" class="form-control" v-model="editData.rarity">
                            </div>
                            <div class="form-col">
                                <label>容量</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.drain">
                            </div>
                            <div class="form-col">
                                <label>最大等级</label>
                                <input type="number" class="form-control number-input" v-model.number="editData.max_rank">
                            </div>
                        </div>
                        <div class="form-row">
                            <div class="form-col">
                                <label>可交易</label>
                                <div class="form-check">
                                    <input type="checkbox" class="form-check-input" v-model="editData.tradable">
                                </div>
                            </div>
                            <div class="form-col">
                                <label>套装</label>
                                <input type="text" class="form-control" v-model="editData.mod_set">
                            </div>
                        </div>
                    </template>

                    <div class="mt-4">
                        <button type="submit" class="btn btn-primary me-2">保存</button>
                        <button type="button" class="btn btn-secondary" @click="cancel">取消</button>
                    </div>
                </form>
            </div>
        </div>
    `,
    watch: {
        item: {
            immediate: true,
            handler(newItem) {
                if (newItem) {
                    this.editData = { ...newItem };
                }
            }
        }
    },
    methods: {
        save() {
            const saveData = { ...this.editData };
            
            // 保持原有的技能数据不变
            if (this.type === 'warframes' && this.item) {
                saveData.abilities_en = this.item.abilities_en;
                saveData.abilities_zh = this.item.abilities_zh;
                saveData.description_en = this.item.description_en;
                saveData.description_zh = this.item.description_zh;
                saveData.passive_en = this.item.passive_en;
                saveData.passive_zh = this.item.passive_zh;
            }
            
            this.$emit('save', saveData);
        },
        cancel() {
            this.$emit('cancel');
        }
    }
}; 