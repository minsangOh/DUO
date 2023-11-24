<template>
  <div class="marg">
    <div>
      <h1>지역별 인기 예금 상품</h1>
    </div>
    <table class="table">
      <th>지역 & 순위</th>
      <th>1</th>
      <th>2</th>
      <th>3</th>
      <tr v-for="(products, location) in tstore.depositlocation" :key="job">
        <th class="col">{{ location }}</th>
        <td>
          <RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: getCD(products[0].product_id) } }" class="link">
            {{ getName(products[0].product_id) }}<br>{{ products[0].count }}명
          </RouterLink>
        </td>
        <td>
          <RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: getCD(products[1].product_id) } }" class="link">
            {{ getName(products[1].product_id) }}<br>{{ products[1].count }}명
          </RouterLink>
        </td>
        <td>
          <RouterLink :to="{ name: 'depositdetail', params: { fin_prdt_cd: getCD(products[2].product_id) } }" class="link">
            {{ getName(products[2].product_id) }}<br>{{ products[2].count }}명
          </RouterLink>
        </td>
      </tr>
    </table>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useTopStore } from '@/stores/top';
import { useFinanceStore } from '@/stores/finance'
const tstore = useTopStore()
const fstore = useFinanceStore()

onMounted(() => {
  tstore.getTopDeposits()
  fstore.getDepositProducts()
})

const getName = function(id) {
  for (const product of fstore.depositList) {
    if (product.id === id) {
      return product.fin_prdt_nm
    }
  }
  return ''; // 못찾으면 ''
}

const getCD = function(id) {
  for (const product of fstore.depositList) {
    if (product.id === id) {
      return product.fin_prdt_cd
    }
  }
  return ''; // 못찾으면 ''
}
</script>

<style scoped>
  .col {
    min-width: 100px;
  }

  .link {
    text-decoration: none;
    color: black;
  }

  .marg {
    margin: 3%;
  }

  .color {
    background-color: #3F445C;
    color: #FFF3EB;
    border-radius: 7%;
  }
</style>
