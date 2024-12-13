<template>
  <DashboardLayout>
    <div class="users-content">
      <div class="page-header">
        <h2>系统管理员</h2>
        <button class="btn-add" @click="showAddUserModal = true">
          <i class="fas fa-plus"></i> 添加管理员
        </button>
      </div>

      <div class="filters">
        <div class="filter-item">
          <label>状态：</label>
          <select v-model="statusFilter">
            <option value="">全部</option>
            <option value="active">活跃</option>
            <option value="inactive">禁用</option>
          </select>
        </div>
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索管理员名称或邮箱..."
          >
        </div>
      </div>

      <div class="users-table">
        <table>
          <thead>
            <tr>
              <th class="border-cell">ID</th>
              <th class="border-cell">管理员名称</th>
              <th class="border-cell">邮箱</th>
              <th class="border-cell">手机号码</th>
              <th class="border-cell">状态</th>
              <th class="border-cell">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in filteredUsers" :key="user.id">
              <td class="border-cell">{{ user.id }}</td>
              <td class="border-cell">{{ user.username }}</td>
              <td class="border-cell">{{ user.email }}</td>
              <td class="border-cell">{{ user.phone || '-' }}</td>
              <td class="border-cell">
                <span :class="['status-badge', user.is_active ? 'active' : 'inactive']">
                  {{ user.is_active ? '活跃' : '禁用' }}
                </span>
              </td>
              <td class="border-cell">
                <button class="btn-edit" @click="editUser(user)">编辑</button>
                <button class="btn-delete" @click="deleteUser(user.id)">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 添加管理员对话框 -->
    <div class="modal" v-if="showAddUserModal">
      <div class="modal-content modal-large">
        <div class="modal-header">
          <h3>{{ isEditing ? '编辑管理员' : '添加管理员' }}</h3>
          <button class="btn-close" @click="closeModal">×</button>
        </div>
        <div class="modal-body">
          <div class="checklist-container">
            <div class="checklist-section">
              <h4>基本信息</h4>
              <div class="form-group">
                <label>用户名 <span class="required">*</span></label>
                <input 
                  type="text" 
                  v-model="newUser.username" 
                  required
                  minlength="2"
                  maxlength="50"
                  placeholder="请输入用户名"
                >
                <span class="hint">用户名长度需要在2-50个字符之间</span>
              </div>
              <div class="form-group">
                <label>邮箱 <span class="required">*</span></label>
                <input 
                  type="email" 
                  v-model="newUser.email" 
                  required
                  pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
                  placeholder="请输入有效的邮箱地址"
                >
              </div>
              <div class="form-group">
                <label>手机号码</label>
                <input 
                  type="tel" 
                  v-model="newUser.phone" 
                  pattern="^1\d{10}$"
                  placeholder="请输入11位手机号码"
                >
                <span class="hint">请输入有效的11位手机号码</span>
              </div>
            </div>

            <div class="checklist-section">
              <h4>安全设置</h4>
              <div class="form-group">
                <label>密码 <span class="required">*</span></label>
                <input 
                  type="password" 
                  v-model="newUser.password" 
                  :required="!isEditing"
                  minlength="6"
                  maxlength="50"
                  placeholder="请输入密码"
                >
                <span class="hint">密码长度需要在6-50个字符之间</span>
              </div>
              <div class="form-group">
                <label>确认密码 <span class="required">*</span></label>
                <input 
                  type="password" 
                  v-model="confirmPassword" 
                  :required="!isEditing"
                  minlength="6"
                  maxlength="50"
                  placeholder="请再次输入密码"
                >
              </div>
            </div>

            <div class="checklist-section">
              <h4>账户设置</h4>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="newUser.is_active">
                  <span>账户激活</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="newUser.is_admin">
                  <span>管理员权限</span>
                </label>
              </div>
            </div>

            <div class="checklist-section">
              <h4>验证清单</h4>
              <div class="checklist-items">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="validationChecklist.emailVerified">
                  <span>邮箱已验证</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="validationChecklist.passwordStrength">
                  <span>密码强度符合要求</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="validationChecklist.termsAccepted">
                  <span>已同意使用条款</span>
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
              @click="submitUser"
              :disabled="!isValidationComplete || !isFormValid"
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
  name: 'Users',
  components: {
    DashboardLayout
  },
  data() {
    return {
      users: [],
      showAddUserModal: false,
      isEditing: false,
      newUser: {
        username: '',
        email: '',
        phone: '',
        password: '',
        is_active: true,
        is_admin: false
      },
      statusFilter: '',
      searchQuery: '',
      confirmPassword: '',
      validationChecklist: {
        emailVerified: false,
        passwordStrength: false,
        termsAccepted: false
      }
    }
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => {
        const matchesStatus = !this.statusFilter || 
          (this.statusFilter === 'active' ? user.is_active : !user.is_active);
        
        const matchesSearch = !this.searchQuery || 
          user.username.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
          user.email.toLowerCase().includes(this.searchQuery.toLowerCase());
        
        return matchesStatus && matchesSearch;
      });
    },
    isValidationComplete() {
      return this.validationChecklist.emailVerified &&
             this.validationChecklist.passwordStrength &&
             this.validationChecklist.termsAccepted;
    },
    isFormValid() {
      if (this.isEditing) return true;
      return this.newUser.password === this.confirmPassword &&
             this.newUser.password.length >= 6;
    }
  },
  async created() {
    await this.loadUsers();
  },
  methods: {
    async loadUsers() {
      try {
        const response = await fetch('/api/admin/users', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          this.users = await response.json();
        }
      } catch (error) {
        console.error('获取用户列表失败:', error);
      }
    },
    editUser(user) {
      this.isEditing = true;
      this.newUser = { ...user };
      this.showAddUserModal = true;
    },
    async deleteUser(userId) {
      if (confirm('确定要删除这个用户吗？')) {
        try {
          const response = await fetch(`/api/admin/users/${userId}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          });
          if (response.ok) {
            this.users = this.users.filter(user => user.id !== userId);
            alert('用户删除成功');
          } else {
            alert('删除用户失败');
          }
        } catch (error) {
          console.error('删除用户失败:', error);
          alert('删除用户时发生错误');
        }
      }
    },
    closeModal() {
      this.showAddUserModal = false;
      this.isEditing = false;
      this.confirmPassword = '';
      this.validationChecklist = {
        emailVerified: false,
        passwordStrength: false,
        termsAccepted: false
      };
      this.newUser = {
        username: '',
        email: '',
        phone: '',
        password: '',
        is_active: true,
        is_admin: false
      };
    },
    async submitUser() {
      if (!this.validateForm()) {
        return;
      }

      try {
        const url = this.isEditing ? 
          `/api/admin/users/${this.newUser.id}` : 
          '/api/admin/users';
        
        const method = this.isEditing ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.newUser)
        });
        
        if (response.ok) {
          await this.loadUsers();
          this.closeModal();
          alert(this.isEditing ? '用户更新成功' : '用户创建成功');
        } else {
          const errorData = await response.json();
          alert(errorData.detail || (this.isEditing ? '更新用户失败' : '创建用户失败'));
        }
      } catch (error) {
        console.error('提交用户数据失败:', error);
        alert('提交用户数据时发生错误');
      }
    },
    validateForm() {
      // 验证用户名
      if (!this.newUser.username || this.newUser.username.length < 2 || this.newUser.username.length > 50) {
        alert('用户名长度需要在2-50个字符之间');
        return false;
      }

      // 验证邮箱
      const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!this.newUser.email || !emailRegex.test(this.newUser.email)) {
        alert('请输入有效的邮箱地址');
        return false;
      }

      // 验证密码（仅在创建新用户时）
      if (!this.isEditing && (!this.newUser.password || this.newUser.password.length < 6 || this.newUser.password.length > 50)) {
        alert('密码长度需要在6-50个字符之间');
        return false;
      }

      // 添加手机号码验证
      if (this.newUser.phone) {
        const phoneRegex = /^1\d{10}$/;
        if (!phoneRegex.test(this.newUser.phone)) {
          alert('请输入有效的11位手机号码');
          return false;
        }
      }

      return true;
    }
  }
}
</script>

<style scoped>
.users-content {
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.filters {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  background: white;
  padding: 1rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-item select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.search-box input {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 250px;
}

.btn-add {
  padding: 0.75rem 1.5rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-add:hover {
  background: #45a049;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
}

.status-badge.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-badge.inactive {
  background: #ffebee;
  color: #c62828;
}

/* 模态框样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
}

.modal-header {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  padding: 1rem;
}

.modal-footer {
  padding: 1rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

.btn-submit {
  padding: 0.5rem 1rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-cancel {
  padding: 0.5rem 1rem;
  background: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

/* 表格样式保持不变 */

.required {
  color: #f44336;
  margin-left: 4px;
}

.hint {
  font-size: 0.875rem;
  color: #666;
  margin-top: 4px;
  display: block;
}

.form-group input:invalid {
  border-color: #f44336;
}

.form-group input:valid {
  border-color: #4CAF50;
}

/* 添加新的表格样式 */
.users-table {
  margin-top: 1rem;
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #ddd;
}

.border-cell {
  border: 1px solid #ddd;
  padding: 1rem;
  text-align: left;
}

th.border-cell {
  background: #f8f9fa;
  font-weight: 600;
  white-space: nowrap;
}

tr:hover {
  background-color: #f5f5f5;
}

.status-badge {
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.875rem;
  display: inline-block;
  min-width: 80px;
  text-align: center;
}

.status-badge.active {
  background: #e8f5e9;
  color: #2e7d32;
}

.status-badge.inactive {
  background: #ffebee;
  color: #c62828;
}

.btn-edit, .btn-delete {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  margin-right: 0.5rem;
  cursor: pointer;
  font-size: 0.875rem;
}

.btn-edit {
  background: #4CAF50;
  color: white;
}

.btn-delete {
  background: #f44336;
  color: white;
}

.btn-edit:hover {
  background: #45a049;
}

.btn-delete:hover {
  background: #d32f2f;
}

/* 修改页面标题样式 */
.page-header h2 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin: 0;
}

/* 修改添加按钮样式 */
.btn-add {
  padding: 0.75rem 1.5rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.btn-add:hover {
  background: #45a049;
}

/* 搜索框样式优化 */
.search-box input {
  width: 300px;
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.875rem;
}

.search-box input:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

/* 添加新的样式，与 Models.vue 相同 */
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

/* 滚动条样式 */
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

/* 添加手机号码输入框的特定样式 */
input[type="tel"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

input[type="tel"]:focus {
  outline: none;
  border-color: #4CAF50;
  box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
}

input[type="tel"]:invalid {
  border-color: #f44336;
}

input[type="tel"]:valid {
  border-color: #4CAF50;
}
</style> 