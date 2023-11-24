<template>
  <div>
    <p><label for="comfirmpassword">비밀번호 확인: </label>
      <input type="password" id="comfirmpassword" v-model.trim="password" />
      <button type="button" @click="comfirmpassword">제출</button>
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const password = ref('')

const comfirmpassword = function () {
  const payload = {
    password: password.value
  };
  store.deleteAccount(payload)
};

</script>

<style></style>