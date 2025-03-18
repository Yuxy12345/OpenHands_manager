<template>
  <div v-if="container">
    如果没有跳转，<a :href="containerUrl" target="_blank">点击访问你的容器</a>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const container = ref(null)
const containerUrl = ref('')

onMounted(async () => {
  const res = await axios.get('/api/container')
  container.value = res.data
  containerUrl.value = `http://localhost:${res.data.port}`
  window.location.href = `http://localhost:${res.data.port}`
})
</script>