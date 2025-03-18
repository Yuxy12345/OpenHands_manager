import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import DashBoard from '../components/DashBoard.vue' // 导入仪表盘组件

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/',
    name: 'Dashboard',
    component: DashBoard,
    meta: { requiresAuth: true } // 添加路由守卫验证
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem('token')

  if (accessToken) {
    // 重新登录后，转到之前的页面
    if (Object.keys(from.query).length !== 0) {
      let redirect = from.query.redirect
      if (to.path === redirect) // 解决无限循环问题
      {
        next()
      }
      else {
        next({ path: redirect }) // 重新登录后，转到之前的页面
      }
    }
  }

  if (accessToken && to.path !== '/login') {
    // 有token 但不是去 login页面
    next()
  }
  else if (accessToken && to.path === '/login') {
    //用户已经登陆，不让访问Login登录界面
    next({ path: from.fullPath })
  }
  else if (!accessToken && to.path !== '/login') {
    // 未登录
    next('/login')
  }
  else {
    next()
  }
})

export default router
