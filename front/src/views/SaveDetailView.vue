<template>
  <div class="marg">
    <nav>
      <RouterLink :to="{ name: 'deposit' }" class="link">정기예금</RouterLink> |
      <RouterLink :to="{ name: 'save' }" class="link">정기적금</RouterLink>
    </nav>
    <div>
      <h1>정기적금 상세</h1>
      <div v-if="cstore.isLogin">
        <div v-if="isSubmitted">
          <button  @click="unjoin(store.save.id)" class="color">가입취소</button>
        </div>
        <div v-else>
          <button @click="join(store.save.id)" class="color">가입하기</button>
        </div>
      </div>
      <div v-else>
        <p>가입하려면 로그인하세요</p>
      </div>
      <!-- store.joinSave
      <br>{{ store.joinSave }} <br>
      len = {{ store.joinSave.length }}
      <br><br>
      cstore.mydata.id = 
      <br>{{ cstore.mydata.id }}
      <br><br>
      store.save.id = 
      <br>{{ store.save.id }} -->
    </div>
    <table class="table">
      <tr>
        <th class="col">공시 제출일</th>
        <td>{{ store.save.dcls_strt_day }}</td>
      </tr>  
      <tr>
        <th class="col">금융회사명</th>
        <td>{{ store.save.kor_co_nm }}</td>
      </tr>
      <tr>
        <th class="col">상품명</th>
        <td>{{ store.save.fin_prdt_nm }}</td>
      </tr>  
      <tr>
        <th class="col">상품 설명</th>
        <td>{{ store.save.etc_note }}</td>
      </tr>  
      <tr>
        <th class="col">가입 제한</th>
        <td>{{ store.save.join_deny }}</td>
      </tr>
      <tr>
        <th class="col">가입 대상</th>
        <td>{{ store.save.join_member }}</td>
      </tr>
      <tr>
        <th class="col">가입 방법</th>
        <td>{{ store.save.join_way }}</td>
      </tr>  
      <tr>
        <th class="col">우대조건</th>
        <td>{{ store.save.spcl_cnd }}</td>
      </tr>
    </table>
  </div>
</template>

<script setup>
import { onBeforeMount, defineProps, ref, watch } from 'vue';
import { useFinanceStore } from '@/stores/finance.js';
import { useCounterStore } from '@/stores/counter.js';

const store = useFinanceStore();
const cstore = useCounterStore();

const props = defineProps({
  fin_prdt_cd: String,
});

const isSubmitted = ref(false);

onBeforeMount(async() => {
  await store.getSave(props.fin_prdt_cd);
  await store.getJoinSave(store.save.id);
  checkIfSubmitted(store.save.id);
});

const checkIfSubmitted = function (id) {
  isSubmitted.value = store.joinSave.some((join) => join.product === id && join.user === cstore.mydata.id);
  console.log('isSubmitted:', isSubmitted.value);
};

const join = function (id) {
  const saveId = store.save.id;

  if (!isSubmitted.value) {
    store.joinOrUnjoinSave(saveId, 'post')
      .then(() => {
        isSubmitted.value = true;
        alert('가입되었습니다.')
      })
      .catch((error) => {
        console.error('Error joining product:', error);
      });
  } else {
    console.error('Product is already joined.');
  }
};

const unjoin = function (id) {
  const saveId = store.save.id;

  if (isSubmitted.value) {
    store.joinOrUnjoinSave(saveId, 'delete')
      .then(() => {
        isSubmitted.value = false;
        alert('가입취소되었습니다.')
      })
      .catch((error) => {
        console.error('Error unjoining product:', error);
      });
  } else {
    console.error('Product is not joined.');
  }
};

watch(isSubmitted, (newValue) => {
  console.log('isSubmitted changed:', newValue);
});
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