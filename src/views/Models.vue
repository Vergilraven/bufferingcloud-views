<template>
  <DashboardLayout>
    <div class="models-content">
      <div class="page-header">
        <h2>模型管理</h2>
        <button class="btn-add" @click="showAddModelModal = true">
          <i class="fas fa-plus"></i> 添加模型
        </button>
      </div>

      <div class="filters">
        <div class="filter-item">
          <label>状态：</label>
          <select v-model="statusFilter">
            <option value="">全部</option>
            <option value="active">已启用</option>
            <option value="inactive">已禁用</option>
          </select>
        </div>
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索模型名称..."
          >
        </div>
      </div>

      <div class="models-table">
        <table>
          <thead>
            <tr>
              <th class="border-cell">ID</th>
              <th class="border-cell">模型名称</th>
              <th class="border-cell">版本</th>
              <th class="border-cell">状态</th>
              <th class="border-cell">更新时间</th>
              <th class="border-cell">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="model in filteredModels" :key="model.id">
              <td class="border-cell">{{ model.id }}</td>
              <td class="border-cell">{{ model.name }}</td>
              <td class="border-cell">{{ model.version }}</td>
              <td class="border-cell">
                <span :class="['status-badge', model.is_active ? 'active' : 'inactive']">
                  {{ model.is_active ? '已启用' : '已禁用' }}
                </span>
              </td>
              <td class="border-cell">{{ model.updated_at }}</td>
              <td class="border-cell">
                <button class="btn-edit" @click="editModel(model)">编辑</button>
                <button class="btn-delete" @click="deleteModel(model.id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 新的添加模型对话框 -->
    <div class="modal" v-if="showAddModelModal">
      <div class="modal-content modal-large">
        <div class="modal-header">
          <h3>{{ isEditing ? '编辑模型' : '添加模型' }}</h3>
          <button class="btn-close" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <div class="checklist-container">
            <div class="checklist-section">
              <h4>基本信息</h4>
              <div class="form-group">
                <label>模型名称 <span class="required">*</span></label>
                <input 
                  type="text" 
                  v-model="newModel.name" 
                  required
                  placeholder="请输入模型名称"
                >
              </div>
              <div class="form-group">
                <label>版本号 <span class="required">*</span></label>
                <input 
                  type="text" 
                  v-model="newModel.version" 
                  required
                  placeholder="例如: 1.0.0"
                >
              </div>
            </div>

            <div class="checklist-section">
              <h4>模型配置</h4>
              <div class="form-group">
                <label>模型类型</label>
                <select v-model="newModel.type">
                  <option value="classification">分类模型</option>
                  <option value="detection">检测模型</option>
                  <option value="segmentation">分割模型</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div class="form-group">
                <label>框架版本</label>
                <select v-model="newModel.framework">
                  <option value="pytorch">PyTorch</option>
                  <option value="tensorflow">TensorFlow</option>
                  <option value="other">其他</option>
                </select>
              </div>
            </div>

            <div class="checklist-section">
              <h4>部署设置</h4>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="newModel.is_active">
                  <span>启用模型</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="newModel.gpu_required">
                  <span>需要GPU</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="newModel.batch_processing">
                  <span>支持批处理</span>
                </label>
              </div>
              <div class="form-group">
                <label>内存要求 (GB)</label>
                <input 
                  type="number" 
                  v-model="newModel.memory_requirement"
                  min="1"
                  step="1"
                >
              </div>
            </div>

            <div class="checklist-section">
              <h4>模型描述</h4>
              <div class="form-group">
                <label>功能描述</label>
                <textarea 
                  v-model="newModel.description" 
                  rows="3"
                  placeholder="请描述模型的主要功能和特点"
                ></textarea>
              </div>
              <div class="form-group">
                <label>使用说明</label>
                <textarea 
                  v-model="newModel.usage_guide" 
                  rows="3"
                  placeholder="请提供模型的使用方法和注意事项"
                ></textarea>
              </div>
            </div>

            <div class="checklist-section">
              <h4>验证清单</h4>
              <div class="checklist-items">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="validationChecklist.dataFormat">
                  <span>输入数据格式已验证</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="validationChecklist.performance">
                  <span>性能测试已完成</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="validationChecklist.compatibility">
                  <span>兼容性测试已完成</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="validationChecklist.documentation">
                  <span>文档已完善</span>
                </label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <div class="validation-message" v-if="!isValidationComplete">
            请完成所有必要的验证项
          </div>
          <div class="button-group">
            <button class="btn-cancel" @click="closeModal">取消</button>
            <button 
              class="btn-submit" 
              @click="submitModel"
              :disabled="!isValidationComplete"
            >
              {{ isEditing ? '保存' : '创建' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'

export default {
  name: 'Models',
  components: {
    DashboardLayout
  },
  data() {
    return {
      models: [],
      showAddModelModal: false,
      isEditing: false,
      newModel: {
        name: '',
        version: '',
        type: 'classification',
        framework: 'pytorch',
        description: '',
        usage_guide: '',
        is_active: true,
        gpu_required: false,
        batch_processing: false,
        memory_requirement: 4
      },
      statusFilter: '',
      searchQuery: '',
      validationChecklist: {
        dataFormat: false,
        performance: false,
        compatibility: false,
        documentation: false
      }
    }
  },
  computed: {
    filteredModels() {
      return this.models.filter(model => {
        const matchesStatus = !this.statusFilter || 
          (this.statusFilter === 'active' ? model.is_active : !model.is_active);
        
        const matchesSearch = !this.searchQuery || 
          model.name.toLowerCase().includes(this.searchQuery.toLowerCase());
        
        return matchesStatus && matchesSearch;
      });
    },
    isValidationComplete() {
      return this.validationChecklist.dataFormat &&
             this.validationChecklist.performance &&
             this.validationChecklist.compatibility &&
             this.validationChecklist.documentation
    }
  },
  async created() {
    await this.loadModels();
  },
  methods: {
    async loadModels() {
      try {
        const response = await fetch('/api/admin/models', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          this.models = await response.json();
        }
      } catch (error) {
        console.error('获取模型列表失败:', error);
      }
    },
    editModel(model) {
      this.isEditing = true;
      this.newModel = { ...model };
      this.showAddModelModal = true;
    },
    async deleteModel(modelId) {
      if (confirm('确定要删除这个模型吗？')) {
        try {
          const response = await fetch(`/api/admin/models/${modelId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          if (response.ok) {
            this.models = this.models.filter(model => model.id !== modelId);
            alert('模型删除成功');
          } else {
            alert('删除模型失败');
          }
        } catch (error) {
          console.error('删除模型失败:', error);
          alert('删除模型时发生错误');
        }
      }
    },
    async submitModel() {
      try {
        const url = this.isEditing ? 
          `/api/admin/models/${this.newModel.id}` : 
          '/api/admin/models';
        
        const method = this.isEditing ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.newModel)
        });
        
        if (response.ok) {
          await this.loadModels();
          this.closeModal();
          alert(this.isEditing ? '模型更新成功' : '模型创建成功');
        } else {
          const errorData = await response.json();
          alert(errorData.detail || (this.isEditing ? '更新模型失败' : '创建模型失败'));
        }
      } catch (error) {
        console.error('提交模型数据失败:', error);
        alert('提交模型数据时发生错误');
      }
    },
    closeModal() {
      this.showAddModelModal = false;
      this.isEditing = false;
      this.newModel = {
        name: '',
        version: '',
        type: 'classification',
        framework: 'pytorch',
        description: '',
        usage_guide: '',
        is_active: true,
        gpu_required: false,
        batch_processing: false,
        memory_requirement: 4
      };
    }
  }
}
</script>

<style scoped>
/* 复用 Users.vue 的样式，并添加一些特定样式 */
.models-content {
  padding: 2rem;
}

/* ... 其他样式与 Users.vue 相同 ... */

.form-group textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
}

.modal-large {
  max-width: 800px !important;
  max-height: 90vh;
  overflow-y: auto;
}

.checklist-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.checklist-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.checklist-section h4 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 1.1rem;
}

.checkbox-group {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 1.2rem;
  height: 1.2rem;
}

.checklist-items {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.validation-message {
  color: #dc3545;
  font-size: 0.9rem;
  margin-right: 1rem;
}

.button-group {
  display: flex;
  gap: 1rem;
}

select {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: white;
}

input[type="number"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn-submit:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* 确保滚动条样式美观 */
.modal-large::-webkit-scrollbar {
  width: 8px;
}

.modal-large::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.modal-large::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.modal-large::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style> 