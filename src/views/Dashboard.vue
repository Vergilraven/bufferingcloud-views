<template>
  <DashboardLayout>
    <div class="dashboard-content">
      <div class="stats-grid">
        <div class="stat-card">
          <h3>总用户数</h3>
          <p class="stat-number">{{ stats.totalUsers }}</p>
        </div>
        <div class="stat-card">
          <h3>活跃用户</h3>
          <p class="stat-number">{{ stats.activeUsers }}</p>
        </div>
        <div class="stat-card">
          <h3>总订单数</h3>
          <p class="stat-number">{{ stats.totalOrders }}</p>
        </div>
      </div>
      
      <div class="recent-activity">
        <h2>最近活动</h2>
        <div class="activity-list">
          <div v-for="activity in recentActivities" 
               :key="activity.id" 
               class="activity-item">
            <span class="activity-time">{{ activity.time }}</span>
            <span class="activity-desc">{{ activity.description }}</span>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'

export default {
  name: 'Dashboard',
  components: {
    DashboardLayout
  },
  data() {
    return {
      stats: {
        totalUsers: 0,
        activeUsers: 0,
        totalOrders: 0
      },
      recentActivities: []
    }
  },
  async created() {
    try {
      const response = await fetch('http://localhost:8000/api/admin/dashboard', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      this.stats = data;
    } catch (error) {
      console.error('获取仪表板数据失败:', error);
    }
  }
}
</script>

<style scoped>
.dashboard-content {
  padding: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
  margin-top: 0.5rem;
}

.recent-activity {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.activity-item {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
}

.activity-time {
  color: #666;
  font-size: 0.9rem;
}
</style> 