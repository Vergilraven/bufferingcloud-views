<template>
  <DashboardLayout>
    <div class="settings-content">
      <h2>系统设置</h2>
      <div class="settings-form">
        <div class="setting-group">
          <h3>基本设置</h3>
          <div class="form-item">
            <label>系统名称</label>
            <input type="text" v-model="settings.systemName" />
          </div>
          <div class="form-item">
            <label>系统描述</label>
            <textarea v-model="settings.description" rows="3"></textarea>
          </div>
        </div>

        <div class="setting-group">
          <h3>邮件设置</h3>
          <div class="form-item">
            <label>SMTP服务器</label>
            <input type="text" v-model="settings.smtpServer" />
          </div>
          <div class="form-item">
            <label>SMTP端口</label>
            <input type="number" v-model="settings.smtpPort" />
          </div>
          <div class="form-item">
            <label>发件人邮箱</label>
            <input type="email" v-model="settings.emailFrom" />
          </div>
        </div>

        <div class="setting-group">
          <h3>安全设置</h3>
          <div class="form-item">
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.enableTwoFactor" />
              启用两步验证
            </label>
          </div>
          <div class="form-item">
            <label class="checkbox-label">
              <input type="checkbox" v-model="settings.enableSSL" />
              强制使用HTTPS
            </label>
          </div>
        </div>

        <div class="form-actions">
          <button class="btn-save" @click="saveSettings">保存设置</button>
          <button class="btn-reset" @click="resetSettings">重置</button>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'

export default {
  name: 'Settings',
  components: {
    DashboardLayout
  },
  data() {
    return {
      settings: {
        systemName: 'BufferingCloud Dashboard',
        description: '',
        smtpServer: '',
        smtpPort: 587,
        emailFrom: '',
        enableTwoFactor: false,
        enableSSL: true
      }
    }
  },
  async created() {
    try {
      const response = await fetch('/api/admin/settings', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        this.settings = { ...this.settings, ...data };
      }
    } catch (error) {
      console.error('获取设置失败:', error);
    }
  },
  methods: {
    async saveSettings() {
      try {
        const response = await fetch('/api/admin/settings', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          },
          body: JSON.stringify(this.settings)
        });
        
        if (response.ok) {
          alert('设置保存成功');
        } else {
          alert('保存设置失败');
        }
      } catch (error) {
        console.error('保存设置失败:', error);
        alert('保存设置时发生错误');
      }
    },
    resetSettings() {
      if (confirm('确定要重置所有设置吗？')) {
        this.created(); // 重新加载设置
      }
    }
  }
}
</script>

<style scoped>
.settings-content {
  padding: 2rem;
}

.settings-form {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 2rem;
}

.setting-group {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eee;
}

.setting-group h3 {
  margin-bottom: 1rem;
  color: #2c3e50;
}

.form-item {
  margin-bottom: 1rem;
}

.form-item label {
  display: block;
  margin-bottom: 0.5rem;
  color: #666;
}

.form-item input[type="text"],
.form-item input[type="number"],
.form-item input[type="email"],
.form-item textarea {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-save, .btn-reset {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.btn-save {
  background: #4CAF50;
  color: white;
}

.btn-reset {
  background: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
}

.btn-save:hover {
  background: #45a049;
}

.btn-reset:hover {
  background: #e8e8e8;
}
</style> 