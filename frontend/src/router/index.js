import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/Login.vue'
import DashBoard from '../components/DashBoard.vue'
import Register from '../components/Register.vue'

const white_list_path = ['/login', '/signup'] // 不需要登录的页面

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/signup',
    name: 'Register',
    component: Register
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

  if (accessToken && !white_list_path.includes(to.path)) {
    // 有token 但不是去白名单页面
    next()
  }
  else if (accessToken && white_list_path.includes(to.path)) {
    // 用户已经登陆，不让访问白名单页面
    next({ path: from.fullPath })
  }
  else if (!accessToken && !white_list_path.includes(to.path)) {
    // 未登录且不在白名单页面
    next('/login')
  }
  else {
    next()
  }
})

export default router
