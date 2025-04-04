<template>
  <div class="register-container">
    <div class="openhands-logo">
      <img src="../../public/openhands.svg" />
    </div>
    <h2 class="login-title">Sign up to OpenHands</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-group">
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required placeholder="Enter your username" />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required placeholder="Enter your password" />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required
          placeholder="Repeat your password" />
      </div>
      <button type="submit">Register</button>
    </form>
    <div class="back-to-login">
      <a href="/login">Back to login</a>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  name: "Register",
  setup() {
    const username = ref("");
    const password = ref("");
    const confirmPassword = ref("");
    const router = useRouter();

    const handleRegister = async () => {
      if (password.value !== confirmPassword.value) {
        alert("Passwords do not match!");
        return;
      }

      try {
        const response = await axios.post("/api/register", {
          username: username.value,
          password: password.value,
        });

        if (response.status === 201) {
          alert("Registration successful!");
          router.push("/login");
        }
      } catch (error) {
        console.error("Registration failed:", error);
        alert("Registration failed. Please try again.");
      }
    };

    return {
      username,
      password,
      confirmPassword,
      handleRegister,
    };
  },
};
</script>

<style scoped>
.register-container {
  max-width: 400px;
  width: 350px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
.back-to-login {
  text-align: center;
  margin-top: 20px;
  padding-top: 10px;
  color: #666;
}
</style>