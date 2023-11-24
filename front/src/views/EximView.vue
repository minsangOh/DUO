<template>
  <div class="marg">
    <h1>환율계산기</h1>
    <div>
      <div class="input-group mb-3">
        <select class="form=select" aria-label="Default select example" v-model="selectedCur" @change="changeCur">
          <option selected>통화 목록</option>
          <option v-for="exim in exims" :key="exim.cur_unit">{{ exim.cur_nm }}</option>
        </select>
        <input type="text" class="form-control" placeholder=foreign_cur v-model="foregin_cur" @input="onForeignCurInput" @click="blankfor">
        <span class="input-group-text color">{{ cur_unit }}</span>
      </div>
      <div class="input-group">
        <input type="text" class="form-control" placeholder=korean_cur v-model="korean_cur" @input="onKoreanCurInput" @click="blankkor">
        <span class="input-group-text color">₩</span>
      </div>
    </div>
    <br>
    <p>엔화, 인도네시아 루피아는 100단위, 나머지는 모두 1단위</p>


    <!-- <p v-if="error">{{ errorMessage }}</p>
    <p v-for="exim in exims">
      통화코드{{ exim.cur_unit }}
      국가명{{ exim.cur_nm }}
      매매기준율 {{ exim.deal_bas_r }}
    </p> -->
  </div>  
</template>


<script setup>
import axios from "axios";
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router'


const exims = ref([])
// const error = ref(false)
// const errorMessage = ref('') // 에러 메시지를 저장할 ref
// const router = useRouter()


const cur_nm = ref(null) // 국가명/통화명


const selectedCur = ref("통화를 선택하세요")
const cur_unit = computed(() => {
  const selectedExim = exims.value.find((exim) => exim.cur_nm === selectedCur.value)
  return selectedExim? selectedExim.cur_unit : ""
})


const foregin_cur = ref("원하는 통화를 선택한 후 숫자만 입력해주세요")
const korean_cur = ref("선택한 통화의 환율이 보입니다")


const fortokor = function() {
  const selectedExim = exims.value.find((exim) => exim.cur_nm === selectedCur.value)


  if (selectedExim) {
    korean_cur.value = foregin_cur.value * selectedExim.deal_bas_r
    return korean_cur
  }
}


const kortofor = function() {
  const selectedExim = exims.value.find((exim) => exim.cur_nm === selectedCur.value)


  if (selectedExim) {
    if (korean_cur.value != "선택한 통화의 환율이 보입니다") {
      // Recalculate foregin_cur based on the new deal_bas_r
      foregin_cur.value = korean_cur.value / selectedExim.deal_bas_r;
    } else {
      foregin_cur.value = "";
    }
    return korean_cur;
  }
}


const numericPattern = /^\d*\.?\d*$/;


const onForeignCurInput = function() {
  if (!numericPattern.test(foregin_cur.value)) {
    foregin_cur.value = foregin_cur.value.replace(/[^0-9.]/g, '');
  }
  fortokor();
};


const onKoreanCurInput = function() {
  if (!numericPattern.test(korean_cur.value)) {
    korean_cur.value = korean_cur.value.replace(/[^0-9.]/g, '');
  }
  kortofor();
};


const changeCur = function() {
  const selectedExim = exims.value.find((exim) => exim.cur_nm === selectedCur.value);


  if (korean_cur.value !== "선택한 통화의 환율이 보입니다") {
    // Calculate foregin_cur based on the new deal_bas_r when korean_cur is not the default value
    foregin_cur.value = korean_cur.value / selectedExim.deal_bas_r;
  } else if (foregin_cur.value !== "원하는 통화를 선택한 후 숫자만 입력해주세요") {
    // Calculate korean_cur based on the new deal_bas_r when foregin_cur is not the default value
    korean_cur.value = foregin_cur.value * selectedExim.deal_bas_r;
  }
}


const blankfor = function() {
  if (foregin_cur.value === "원하는 통화를 선택한 후 숫자만 입력해주세요") {
    foregin_cur.value = ''
  }
}


const blankkor = function() {
  if (korean_cur.value === "선택한 통화의 환율이 보입니다") {
    korean_cur.value = ''
  }
}


// 환율정보 back에서 가져오기
const EXIM_URL = `http://localhost:8000/apis/exim/`


const getExim = function() {
  axios.get(EXIM_URL)
    .then((res) => {
      exims.value = res.data.response.map(exim => ({
        ...exim,
        deal_bas_r: exim.deal_bas_r.replace(/,/g, ''), // ,가 deal_bas_r에 있어서 NaN이 나옴 => 업애는 코드!!!
      }));
      console.log(exims);
    })
    .catch((e) => {console.log(e)})
}


onMounted(() => {
  getExim()
})




</script>


<style scoped>
.marg {
  margin: 3%;
}

.color {
  background-color: #3F445C;
  color: #FFF3EB;
}
</style>

