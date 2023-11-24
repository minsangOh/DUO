<template>
  <div class="marg">
    <main v-if="user">
      <h1>{{ user.username }}님의 프로필 정보</h1>
      <p>아이디: {{ user.username }}</p>
      <p>이메일 주소: {{ user.email }}</p>
      <p>닉네임: {{ user.nickname }}</p>
      <p>나이: {{ user.age }}</p>
      <!-- <p>현재 자산 총액: {{ user.money }}</p> -->
      <!-- <p>월간 수입: {{ user.salary }}</p> -->
      <!-- <p>직업: {{ user.job }}</p> -->
      <!-- <p>거주지: {{ user.location }}</p> -->
      <!-- <p>가입 상품 목록(예금): {{ user.financial_products_deposit }}</p>
      <p>가입 상품 목록(적금): {{ user.financial_products_save }}</p> -->
    </main>
    <div v-else-if="isLoading">
      로딩 중...
    </div>
    <div v-else>
      사용자 정보를 불러오는 데 실패했습니다.
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref, watch } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'

const store = useCounterStore()
const route = useRoute()
const user = ref(null)
const isLoading = ref(false)

// 사용자 정보를 불러오는 함수
const fetchUserData = () => {
  isLoading.value = true
  axios({
    method: 'get',
    url: `${store.API_URL}/accounts/user/${route.params.id}/`
  })
    .then((res) => {
      user.value = res.data
    })
    .catch((err) => {
      console.error(err)
    })
    .finally(() => {
      isLoading.value = false
    })
}

onMounted(fetchUserData)

// route.params.id가 변경될 때마다 사용자 정보 다시 불러오기
watch(() => route.params.id, fetchUserData)
</script>


<style scoped>
.marg {
  margin: 3%;
}
</style>
