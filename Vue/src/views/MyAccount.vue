<template>
  <div class="container">
    <!-- Your Property: Left -->
    <div class="account-view left">
      <h2 class="property-title">Your Property</h2>
      <div class="property">
        <div class="property-item total">
          <span>Total  全额:</span> {{ formatCurrency(total) }}
        </div>
        <div class="property-item current">
          <span>Current  活期:</span> {{ formatCurrency(current) }}
        </div>
        <div class="property-item deposit">
          <span>Deposit  定存:</span> {{ formatCurrency(deposit) }}
        </div>
        <div class="property-item fin-service">
          <span>Investing  定投:</span> {{ formatCurrency(investing) }}
        </div>
      </div>
    </div>

    <!-- Your Property: Right -->
    <div class="account-view right">
      <div class="user-info">
        <img src="./marple.png" alt="User Image" class="user-image">
        <div class="user-details">
          <p>User: Hercule Poirot</p>
          <p>Credit Card: 1</p>
          <p>Debit Card: 1</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      current: 10000.00,
      deposit: 50000.00,
      investing: 25000.78
    };
  },
  computed: {
    total() {
      return this.current + this.deposit + this.investing;
    }
  },
  methods: {
    formatCurrency(value) {
      return new Intl.NumberFormat("zh-CN", { style: "currency", currency: "CNY" }).format(value);
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
}

.account-view {
  padding: 40px;
  background-color: #f5f5f5;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 600px;
  max-width: 800px;
  height: 600px;
  margin: 20px;
}

.property-title {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 32px;
}

.property {
  display: flex;
  flex-direction: column;
}

.property-item {
  margin-bottom: 20px;
  padding: 20px;
  background-color: #fff;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.property-item span {
  font-weight: bold;
  font-size: 24px;
}

.property-item.total {
  border-color: #4caf50;
}

.property-item.current {
  border-color: #2196f3;
}

.property-item.deposit {
  border-color: #ff9800;
}

.property-item.fin-service {
  border-color: #f44336;
}

.left {
  align-self: flex-start;
}

.right {
  align-self: center;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-image {
  max-width: 100%;
  height: auto;
  max-height: 200px;
  margin-bottom: 20px;
}

.user-details {
  font-size: 28px;
}

.user-text {
  font-size: 24px;
}
</style>
