<template>
  <div>
    <!-- 加载遮罩 -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="load_animation">
        <div></div><div></div>
      </div>
      <div class="loading-message">
        容器正在准备中，第一次启动或最近没有访问可能时间稍长，请稍等...
      </div>
    </div>

    <!-- 其他内容 -->
    <div v-if="container">
      如果没有跳转，<a :href="containerUrl" target="_blank">点击访问你的容器</a>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      isLoading: false, // 控制加载遮罩的显示
      container: null,
      containerUrl: '',
    };
  },
  mounted() {
    this.fetchContainer();
  },
  methods: {
    async fetchContainer() {
      try {
        this.isLoading = true; // 显示加载遮罩
        const response = await axios.get('/api/container');
        this.container = response.data;
        this.containerUrl = `http://localhost:${response.data.port}`;
        window.location.href = `http://localhost:${response.data.port}`;
      } catch (error) {
        console.error('请求失败:', error);
      } finally {
        this.isLoading = false; // 隐藏加载遮罩
      }
    },
  },
};
</script>

<style>
/* 加载遮罩样式 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-message {
  color: white;
  font-size: 18px;
  text-align: center;
  padding: 20px;
  background: rgba(0, 0, 0, 0.8);
  border-radius: 8px;
}

.load_animation{
  display: inline-block;
  position: relative;
  width: 64px;
  height: 64px;
}
.load_animation div{
  position: absolute;
  border: 4px solid #61E8EA;
  opacity: 1;
  border-radius: 50%;
  animation: load_animation 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
}
.load_animation div:nth-child(2) {
  animation-delay: -0.5s;
}
@keyframes load_animation{
  0% {
    top: 28px;
    left: 28px;
    width: 0;
    height: 0;
    opacity: 1;
  }
  100% {
    top: -1px;
    left: -1px;
    width: 58px;
    height: 58px;
    opacity: 0;
  }
}
</style>