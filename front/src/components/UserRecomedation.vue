<template>
  <div>
    <br>
    <!-- 추천 정기 예금 상품 표시 -->
    <div v-if="recommendationsLoaded" class="product-display">
      <h2>추천 정기 예금 상품</h2>
      <div v-if="recommendations.length" class="card-container">
        <div class="card">
          <button @click="prevProduct('deposit')" class="arrow left">←</button>
          <div class="card-content" v-for="(product, index) in recommendations" :key="product.fin_prdt_cd"
            v-show="currentDepositIndex === index">
            <RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: product.fin_prdt_cd } }">
              <h3>{{ product.kor_co_nm }} - {{ product.product_name }}</h3>
            </RouterLink>
            <p>상품 가입자수: {{ product.num_joins }}</p>
            <p>{{ product.details }}</p>
            <li v-for="option in product.options" :key="option.id">
              금리: {{ option.intr_rate }}%, 우대금리: {{ option.intr_rate2 }}%, 저축 기간: {{ option.save_trm }}개월
            </li>
          </div>
          <button @click="nextProduct('deposit')" class="arrow right">→</button>
        </div>
      </div>
      <p v-else>추천할 상품이 없습니다.</p>
    </div>
    <br>
    <!-- 추천 정기 적금 상품 표시 -->
    <div v-if="savingsRecommendationsLoaded" class="product-display">
      <h2>추천 정기 적금 상품</h2>
      <div v-if="savingsRecommendations.length" class="card-container">
        <div class="card">
          <button @click="prevProduct('savings')" class="arrow left">←</button>
          <div class="card-content" v-for="(product, index) in savingsRecommendations" :key="product.fin_prdt_cd"
            v-show="currentSavingsIndex === index">
            <RouterLink :to="{ name: 'savedetail', params: { fin_prdt_cd: product.fin_prdt_cd } }">
              <h3>{{ product.kor_co_nm }} - {{ product.product_name }}</h3>
            </RouterLink>
            <p>해당 상품 가입자수: {{ product.num_joins }}</p>
            <p>상품 가입자수: {{ product.num_joins }}</p>
            <p>{{ product.details }}</p>
            <li v-for="option in product.options" :key="option.id">
              금리: {{ option.intr_rate }}%, 우대금리: {{ option.intr_rate2 }}%, 저축 기간: {{ option.save_trm }}개월
            </li>

          </div>
          <button @click="nextProduct('savings')" class="arrow right">→</button>
        </div>
      </div>
      <p v-else>추천할 적금 상품이 없습니다.</p>
    </div>

  </div>
</template>



<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { RouterLink } from 'vue-router';

const props = defineProps({
  userId: Number
});

const recommendations = ref([]);
const recommendationsLoaded = ref(false);
const currentDepositIndex = ref(0);

const savingsRecommendations = ref([]);
const savingsRecommendationsLoaded = ref(false);
const currentSavingsIndex = ref(0);

const nextProduct = (type) => {
  if (type === 'deposit' && currentDepositIndex.value < recommendations.value.length - 1) {
    currentDepositIndex.value++;
  } else if (type === 'savings' && currentSavingsIndex.value < savingsRecommendations.value.length - 1) {
    currentSavingsIndex.value++;
  }
};

const prevProduct = (type) => {
  if (type === 'deposit' && currentDepositIndex.value > 0) {
    currentDepositIndex.value--;
  } else if (type === 'savings' && currentSavingsIndex.value > 0) {
    currentSavingsIndex.value--;
  }
};

onMounted(() => {
  if (props.userId) {
    // 추천 예금 상품 불러오기
    axios.get(`http://127.0.0.1:8000/accounts/recommend_products_deposit/${props.userId}`)
      .then(response => {
        recommendations.value = response.data.products;
        recommendationsLoaded.value = true;
      })
      .catch(error => {
        console.error('추천 예금 상품을 불러오는데 실패했습니다:', error);
        recommendationsLoaded.value = true;
      });

    // 추천 적금 상품 불러오기
    axios.get(`http://127.0.0.1:8000/accounts/recommend_products_save/${props.userId}`)
      .then(response => {
        savingsRecommendations.value = response.data.products;
        savingsRecommendationsLoaded.value = true;
      })
      .catch(error => {
        console.error('추천 적금 상품을 불러오는데 실패했습니다:', error);
        savingsRecommendationsLoaded.value = true;
      });
  }
});
</script>


<style lang="scss" scoped>
.product-display {
  .card-container {
    position: relative;
    max-width: 100%;
    margin: auto;
  }

  .card {
    border: 1px solid #ccc;
    display: flex;
    align-items: center;
    position: relative; // 화살표를 위한 상대 위치 설정
  }

  .card-content {
    flex-grow: 1;
    padding: 16px;
    padding-left: 50px; // 왼쪽 화살표를 위한 공간 확보
    padding-right: 50px; // 오른쪽 화살표를 위한 공간 확보
    box-sizing: border-box; // 패딩을 포함한 너비를 유지
  }

  .arrow {
    background-color: transparent;
    border: none;
    cursor: pointer;
    width: 50px; // 화살표 버튼의 너비 설정
    height: 100%; // 카드와 동일한 높이 설정
    display: flex;
    align-items: center; // 수직 중앙 정렬
    justify-content: center; // 수평 중앙 정렬
    position: absolute;
    top: 50%;
    transform: translateY(-50%); // 화살표 버튼을 수직 중앙으로 정렬
  }

  .left {
    left: 0;
  }

  .right {
    right: 0;
  }
}
</style>
