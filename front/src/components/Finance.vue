<template>
  <div class="marg">
    <nav>
      <RouterLink :to="{ name: 'deposit' }" class="link">정기예금</RouterLink> |
      <RouterLink :to="{ name: 'save' }" class="link">정기적금</RouterLink>
    </nav>

    <div v-if="isDepositOrSaveRoute">
      <RouterView />
    </div>

    <div v-else>
      <h1>이 상품 목록은 금융감독원 금융상품통합비교공시 API를 활용하였습니다.</h1>
      <img src="@/assets/FSSCI.jpg" alt="금융분석 이미지" />
    </div>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
import { onMounted, computed, getCurrentInstance } from 'vue';
import { useFinanceStore } from '@/stores/finance';

const instance = getCurrentInstance();
const store = useFinanceStore();

onMounted(() => {
  store.getDepositProducts();
  store.getSaveProducts();
});

const isDepositOrSaveRoute = computed(() => {
  const currentRoute = instance.proxy.$route.name;
  return currentRoute === 'deposit' || currentRoute === 'save';
});
</script>



<style scoped>
.link {
  text-decoration: none;
  color: black;
}

img {
  width: 80%;

}

.marg {
  margin: 3%;
}
</style>
