<template>
  <div class="dashboard-container">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3>控制面板</h3>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-item">
          <i class="fas fa-home"></i>
          概览
        </router-link>
        <router-link to="/dashboard/users" class="nav-item">
          <i class="fas fa-users"></i>
          系统管理员
        </router-link>
        <router-link to="/dashboard/models" class="nav-item">
          <i class="fas fa-cube"></i>
          模型管理
        </router-link>
        <router-link to="/dashboard/settings" class="nav-item">
          <i class="fas fa-cog"></i>
          系统设置
        </router-link>
        <router-link to="/dashboard/trading" class="nav-item">
          <i class="fas fa-chart-line"></i>
          量化交易
        </router-link>
      </nav>
    </aside>
    
    <main class="main-content">
      <header class="top-bar">
        <div class="search-box">
          <input type="search" placeholder="搜索...">
        </div>
        <div class="user-menu">
          <span class="username">管理员</span>
          <button @click="handleLogout" class="logout-btn">
            退出登录
          </button>
        </div>
      </header>
      
      <div class="content-area">
        <slot></slot>
        
        <div class="system-info">
          <span class="system-name">BufferingCloud Dashboard</span>
          <span class="version">v1.0.1</span>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'DashboardLayout',
  data() {
    return {
      systemInfo: {
        name: 'BufferingCloud Dashboard',
        version: 'v1.0.1'
      }
    }
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  }
}
</script>

<style scoped>
.dashboard-container {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 250px;
  background: #2c3e50;
  color: white;
  padding: 1rem;
}

.sidebar-header {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-nav {
  margin-top: 2rem;
}

.nav-item {
  display: block;
  padding: 1rem;
  color: white;
  text-decoration: none;
  transition: background-color 0.3s;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
}

.main-content {
  flex: 1;
  background: #f5f6fa;
}

.top-bar {
  background: white;
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.search-box input {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 300px;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-btn {
  padding: 0.5rem 1rem;
  background: #e74c3c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.content-area {
  padding: 2rem;
  position: relative;
  min-height: calc(100vh - 64px);
  padding-bottom: 3rem;
}

.system-info {
  position: fixed;
  bottom: 1rem;
  right: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-size: 0.875rem;
  color: #666;
  z-index: 100;
}

.system-name {
  font-weight: 500;
}

.version {
  color: #999;
  font-size: 0.75rem;
}

.system-info:hover {
  background: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style> 