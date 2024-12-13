<template>
  <DashboardLayout>
    <div class="trading-content">
      <div class="page-header">
        <h2>量化交易</h2>
        <div class="search-box">
          <input 
            type="text" 
            v-model="searchSymbol"
            placeholder="输入股票代码..."
            @keyup.enter="searchStock"
          >
          <button class="btn-search" @click="searchStock">
            <i class="fas fa-search"></i> 搜索
          </button>
        </div>
      </div>

      <div class="trading-grid">
        <!-- 股票信息卡片 -->
        <div class="stock-card" v-if="stockInfo">
          <div class="stock-header">
            <h3>{{ stockInfo.name }}</h3>
            <span class="symbol">{{ stockInfo.symbol }}</span>
          </div>
          <div class="price-info">
            <div class="current-price">
              ${{ stockInfo.price }}
              <span :class="['change', stockInfo.change >= 0 ? 'positive' : 'negative']">
                {{ stockInfo.change >= 0 ? '+' : '' }}{{ stockInfo.changePercent.toFixed(2) }}%
              </span>
            </div>
          </div>
          <div class="trading-stats">
            <div class="stat-item">
              <span class="label">开盘</span>
              <span class="value">${{ stockInfo.open }}</span>
            </div>
            <div class="stat-item">
              <span class="label">最高</span>
              <span class="value">${{ stockInfo.high }}</span>
            </div>
            <div class="stat-item">
              <span class="label">最低</span>
              <span class="value">${{ stockInfo.low }}</span>
            </div>
            <div class="stat-item">
              <span class="label">成交量</span>
              <span class="value">{{ formatVolume(stockInfo.volume) }}</span>
            </div>
          </div>
        </div>

        <!-- 技术指标卡片 -->
        <div class="indicators-card" v-if="indicators">
          <h3>技术指标</h3>
          <div class="indicators-grid">
            <div class="indicator-item">
              <span class="label">MA5</span>
              <span class="value">${{ indicators.ma5.toFixed(2) }}</span>
            </div>
            <div class="indicator-item">
              <span class="label">MA10</span>
              <span class="value">${{ indicators.ma10.toFixed(2) }}</span>
            </div>
            <div class="indicator-item">
              <span class="label">MA20</span>
              <span class="value">${{ indicators.ma20.toFixed(2) }}</span>
            </div>
            <div class="indicator-item">
              <span class="label">RSI</span>
              <span class="value">{{ indicators.rsi.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <!-- K线图表 -->
        <div class="chart-card">
          <div class="chart-header">
            <h3>价格走势</h3>
            <div class="chart-controls">
              <select v-model="period">
                <option value="1d">1天</option>
                <option value="5d">5天</option>
                <option value="1mo">1月</option>
                <option value="3mo">3月</option>
                <option value="6mo">6月</option>
                <option value="1y">1年</option>
              </select>
              <select v-model="interval">
                <option value="1m">1分钟</option>
                <option value="5m">5分钟</option>
                <option value="15m">15分钟</option>
                <option value="30m">30分钟</option>
                <option value="1h">1小时</option>
                <option value="1d">1天</option>
              </select>
            </div>
          </div>
          <div class="chart-container">
            <!-- 这里可以使用 ECharts 或其他图表库 -->
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script>
import DashboardLayout from '@/components/DashboardLayout.vue'

export default {
  name: 'Trading',
  components: {
    DashboardLayout
  },
  data() {
    return {
      searchSymbol: '',
      stockInfo: null,
      indicators: null,
      history: [],
      period: '1mo',
      interval: '1d'
    }
  },
  methods: {
    async searchStock() {
      if (!this.searchSymbol) return;
      
      try {
        // 获取股票报价
        const quoteResponse = await fetch(`/api/stock/quote/${this.searchSymbol}`);
        if (quoteResponse.ok) {
          this.stockInfo = await quoteResponse.json();
        }

        // 获取技术指标
        const indicatorsResponse = await fetch(`/api/stock/indicators/${this.searchSymbol}`);
        if (indicatorsResponse.ok) {
          this.indicators = await indicatorsResponse.json();
        }

        // 获取历史数据
        await this.loadHistory();
      } catch (error) {
        console.error('获取股票数据失败:', error);
        alert('获取股票数据失败');
      }
    },
    async loadHistory() {
      try {
        const response = await fetch(
          `/api/stock/history/${this.searchSymbol}?period=${this.period}&interval=${this.interval}`
        );
        if (response.ok) {
          this.history = await response.json();
          // 这里可以更新图表
        }
      } catch (error) {
        console.error('获取历史数据失败:', error);
      }
    },
    formatVolume(volume) {
      if (volume >= 1000000) {
        return (volume / 1000000).toFixed(2) + 'M';
      }
      if (volume >= 1000) {
        return (volume / 1000).toFixed(2) + 'K';
      }
      return volume;
    }
  },
  watch: {
    period() {
      this.loadHistory();
    },
    interval() {
      this.loadHistory();
    }
  }
}
</script>

<style scoped>
.trading-content {
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.search-box {
  display: flex;
  gap: 1rem;
}

.search-box input {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

.btn-search {
  padding: 0.5rem 1rem;
  background: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.trading-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.stock-card, .indicators-card, .chart-card {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.stock-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.symbol {
  color: #666;
  font-size: 0.875rem;
}

.price-info {
  margin-bottom: 1.5rem;
}

.current-price {
  font-size: 2rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.change {
  font-size: 1rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}

.positive {
  background: #e8f5e9;
  color: #2e7d32;
}

.negative {
  background: #ffebee;
  color: #c62828;
}

.trading-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
}

.label {
  color: #666;
  font-size: 0.875rem;
}

.value {
  font-weight: 500;
}

.indicators-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-controls {
  display: flex;
  gap: 1rem;
}

.chart-controls select {
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.chart-container {
  height: 400px;
  background: #f8f9fa;
  border-radius: 4px;
}
</style> 