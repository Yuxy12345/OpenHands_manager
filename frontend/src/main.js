import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import axios from 'axios'

createApp(App).use(router).mount('#app')

axios.interceptors.request.use(
  config => {
    if (localStorage.getItem("token")) {
      config.headers.Authorization = `Bearer ${localStorage.getItem("token")}`
    }
    return config;
  },
  err => {
    return Promise.reject(err);
  }
)

axios.interceptors.response.use(
  response => {
    return response;
  },
  error => {
    if (error.response) {
      console.log('axios:' + error.response.status);
      switch (error.response.status) {
        case 403:
        case 401:
          // 返回403 清除token信息并跳转到登录页面
          localStorage.clear()
          router.replace({
            path: '/login',
            query: { redirect: router.currentRoute.fullPath }   // 重新登录后，返回之前的页面
          })
      }
    }
    return Promise.reject(error);   // 返回接口的错误信息
  }
)
