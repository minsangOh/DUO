<template>
  <div>
    <div class="sign-in">
      <form @submit.prevent="logIn">
        user: <input type="text" placeholder="Username" v-model.trim="username" />
        <div><br></div>

        p.w: <input type="password" placeholder="Password" v-model.trim="password" />
        <div><br></div>
        <input type="submit" value="Sign in" />
        <hr>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const username = ref('')
const password = ref('')

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}

</script>

<style></style>