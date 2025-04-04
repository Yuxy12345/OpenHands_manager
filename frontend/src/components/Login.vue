<template>
  <div class="login-container">
    <div class="login-box">
      <div class="openhands-logo">
        <img src="../../public/openhands.svg"/>
      </div>

      <h2 class="login-title">Sign in to OpenHands</h2>

      <form @submit.prevent="login">
        <div class="input-group">
          <label for="username">Username or email</label>
          <input type="text" id="username" v-model="username" required />
        </div>

        <div class="input-group">
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <button type="submit" class="login-button">
          Sign in
        </button>
      </form>

      <div class="auth-links">
        <a href="#" class="forgot-password">Forgot password?</a>
        <br />
        <a href="/signup" class="signup-link">New to OpenHands? Sign up</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const router = useRouter()

const login = async () => {
  try {
    const res = await axios.post('/api/login', {
      username: username.value,
      password: password.value
    })
    localStorage.setItem('token', res.data.access_token)
    router.push('/')
  } catch (error) {
    if (error.response && error.response.data && error.response.data.error) {
      alert(error.response.data.error)
    } else {
      alert('An unexpected error occurred.')
    }
  }

  localStorage.setItem('token', res.data.access_token)
  router.push('/')
}
</script>

<style lang="css">
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #fff;
}

.login-box {
  width: 350px;
  padding: 40px;
  background-color: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.github-logo {
  margin-bottom: 20px;
  text-align: center;
}

.login-title {
  font-size: 20px;
  color: #333;
  margin-bottom: 15px;
}

.input-group {
  margin-bottom: 15px;
}

input-group label {
  display: block;
  margin-bottom: 5px;
  color: #666;
  font-size: 14px;
}

input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 3px;
  box-sizing: border-box;
}

.login-button {
  width: 100%;
  padding: 9px 16px;
  background-color: #1DA1F2;
  color: white;
  border: none;
  border-radius: 3px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color .5s;
}

.login-button:hover {
  background-color: #009dff;
}

.auth-links {
  margin-top: 20px;
  text-align: center;
}

.auth-links a {
  color: #666;
  text-decoration: none;
}

.forgot-password {
  color: #666;
}

.signup-link {
  display: block;
  margin-top: 5px;
}
</style>
