<template>
  <div>
    <div>
      <h2>검색하기</h2>
      <div class="input-group mb-3">
        <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">금융회사명</button>
        <ul class="dropdown-menu">
          <li v-for="company in uniqueCompanies" :key="company">
          <a class="dropdown-item" @click="filterByCompany(company)">{{ company }}</a>
        </li>
        </ul>
        <div class="input-group-text flipcolor">
          <label for="trm6">6개월</label>
          <input class="form-check-input mt-0 color" type="checkbox" id="trm6" v-model="trm6" aria-label="Checkbox for following text input">
        </div>
        <div class="input-group-text flipcolor">
          <label for="trm12">12개월</label>
          <input class="form-check-input mt-0 color" type="checkbox" id="trm12" v-model="trm12" aria-label="Checkbox for following text input">
        </div>
        <div class="input-group-text flipcolor">
          <label for="trm24">24개월</label>
          <input class="form-check-input mt-0 color" type="checkbox" id="trm24" v-model="trm24" aria-label="Checkbox for following text input">
        </div>
        <div class="input-group-text flipcolor">
          <label for="trm36">36개월</label>
          <input class="form-check-input mt-0 color" type="checkbox" id="trm36" v-model="trm36" aria-label="Checkbox for following text input">
        </div>
      </div>
    </div>
    <h1>정기예금</h1>
    <p>*이자율 정보가 없는 구간은 0으로 표시됩니다.</p>
    <table class="table table-hover">
      <thead>
        <tr>
          <th style="color: black;">공시 제출일</th>
          <th style="color: black;">금융회사명</th>
          <th style="color: black;">상품명</th>
          <th style="color: black;" v-if="trm6" @click="sortTable('intr_rate_6')">6개월<br>Click to sort</th>
          <th style="color: black;" v-if="trm12" @click="sortTable('intr_rate_12')">12개월<br>Click to sort</th>
          <th style="color: black;" v-if="trm24" @click="sortTable('intr_rate_24')">24개월<br>Click to sort</th>
          <th style="color: black;" v-if="trm36" @click="sortTable('intr_rate_36')">36개월<br>Click to sort</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in filteredProducts" :key="product.fin_prdt_cd">
          <td><RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: product.fin_prdt_cd } }" class="link" :fin_prdt_cd="product.fin_prdt_cd">{{ product.dcls_strt_day }}</RouterLink></td>
          <td><RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: product.fin_prdt_cd } }" class="link" :fin_prdt_cd="product.fin_prdt_cd">{{ product.kor_co_nm }}</RouterLink></td>
          <td><RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: product.fin_prdt_cd } }" class="link" :fin_prdt_cd="product.fin_prdt_cd">{{ product.fin_prdt_nm }}</RouterLink></td>
          <td v-if="trm6"><RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: product.fin_prdt_cd } }" class="link" :fin_prdt_cd="product.fin_prdt_cd">{{ product.intr_rate_6 }}</RouterLink></td>
          <td v-if="trm12"><RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: product.fin_prdt_cd } }" class="link" :fin_prdt_cd="product.fin_prdt_cd">{{ product.intr_rate_12 }}</RouterLink></td>
          <td v-if="trm24"><RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: product.fin_prdt_cd } }" class="link" :fin_prdt_cd="product.fin_prdt_cd">{{ product.intr_rate_24 }}</RouterLink></td>
          <td v-if="trm36"><RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: product.fin_prdt_cd } }" class="link" :fin_prdt_cd="product.fin_prdt_cd">{{ product.intr_rate_36 }}</RouterLink></td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useFinanceStore } from '@/stores/finance';
import { onMounted, ref, computed } from 'vue';
import { RouterLink } from 'vue-router';

const store = useFinanceStore();
onMounted(() => {
  store.getDepositOptions();
})

const trm6 = ref(true)
const trm12 = ref(true)
const trm24 = ref(true)
const trm36 = ref(true)

const uniqueCompanies = computed(() => {
  // Extract unique financial company names from the products
  return [...new Set(store.depositOptions.map(product => product.kor_co_nm))];
});

const selectedCompany = ref('');

const filteredProducts = computed(() => {
  // Filter products based on the selected financial company name
  if (selectedCompany.value === '') {
    return store.depositOptions;
  } else {
    return store.depositOptions.filter(product => product.kor_co_nm === selectedCompany.value);
  }
});

function filterByCompany(company) {
  selectedCompany.value = company;
}

const sortOrders = {
  intr_rate_6: 1,
  intr_rate_12: 1,
  intr_rate_24: 1,
  intr_rate_36: 1,
};

function sortTable(column) {
  sortOrders[column] = -sortOrders[column];
  store.depositOptions.sort((a, b) => {
    const aValue = a[column] || 0;
    const bValue = b[column] || 0;

    return sortOrders[column] * (aValue - bValue);
  });
}
</script>

<style scoped>
.link {
  text-decoration: none;
  color: black;
}

.color {
  background-color: #3F445C;
  color: #FFF3EB;
}

.flipcolor { 
  background-color: #FFF3EB;
  color: #3F445C;
}
</style>