<template>
  <main v-if="infoLoaded" class="marg">
    <h1>{{ info.username }}님의 프로필 정보</h1>
    <p>아이디: {{ info.username }}</p>
    <p>이메일 주소: {{ info.email }}</p>
    <p>
      닉네임:
      <span v-if="!isEditing.nickname">{{ info.nickname }}</span>
      <input v-else v-model="editableFields.nickname" type="text">
      <button @click="toggleEdit('nickname')" class="color">{{ isEditing.nickname ? '완료' : '수정' }}</button>
    </p>
    <p>
      나이:
      <span v-if="!isEditing.age">{{ info.age }}</span>
      <input v-else v-model.number="editableFields.age" type="number">
      <button @click="toggleEdit('age')" class="color">{{ isEditing.age ? '완료' : '수정' }}</button>
    </p>
    <p>
      현재 자산 총액:
      <span v-if="!isEditing.money">{{ formatNumber(info.money) }} 원</span>
      <input v-else v-model.number="editableFields.money" type="number">
      <button @click="toggleEdit('money')" class="color">{{ isEditing.money ? '완료' : '수정' }}</button>
    </p>
    <p>
      월간 수입:
      <span v-if="!isEditing.salary">{{ formatNumber(info.salary) }} 원</span>
      <input v-else v-model.number="editableFields.salary" type="number">
      <button @click="toggleEdit('salary')" class="color">{{ isEditing.salary ? '완료' : '수정' }}</button>
    </p>
    <p>
      현재 직업:
      <span v-if="!isEditing.job">{{ info.job }}</span>
      <select v-else v-model="editableFields.job">
        <option value="" disabled>Select Job</option>
        <option value="management">경영/사무/금융/보험직</option>
        <option value="engineering">연구직 및 공학 기술직</option>
        <option value="education">교육/법률/사회복지/경찰/소방직 및 군인</option>
        <option value="health">보건/의료직</option>
        <option value="arts">예술/디자인/방송/스포츠직</option>
        <option value="service">미용/여행/숙박/음식/경비/청소직</option>
        <option value="sales">영업/판매/운전/운송직</option>
        <option value="construction">건설/채굴직</option>
        <option value="production">설치/정비/생산직</option>
        <option value="agriculture">농림어업직</option>
      </select>
      <button @click="toggleEdit('job')" class="color">{{ isEditing.job ? '완료' : '수정' }}</button>
    </p>
    <p>
      거주지:
      <span v-if="!isEditing.location">{{ info.location }}</span>
      <input v-else v-model="editableFields.location" type="text">
      <button @click="openPostcode" class="color">{{ isEditing.location ? '완료' : '수정' }}</button>
    </p>
    <p>가입한 예금 상품 목록:</p>
    <ul>
      <li v-for="deposit in info.joined_deposits" :key="deposit">{{ deposit }}</li>
    </ul>
    <p>가입한 적금 상품 목록:</p>
    <ul>
      <li v-for="saving in info.joined_savings" :key="saving">{{ saving }}</li>
    </ul> <button @click="submitChanges" class="color">변경 사항 저장</button>
    <UserRecomedation :userId="info.id" />
  </main>
</template>

<script setup>
import UserRecomedation from '@/components/UserRecomedation.vue';
import { onMounted, reactive, ref } from 'vue';
import { useCounterStore } from '@/stores/counter';
import axios from 'axios';

const store = useCounterStore();
const info = ref({}); // info를 ref 객체로 초기화
const modifiyInfo = ref({})
const infoLoaded = ref(false); // 데이터 로딩 상태를 추적하는 변수


// 서버에서 데이터를 불러와 info에 할당
onMounted(async () => {
  const latestData = await store.myInfo();
  if (latestData) {
    info.value = { ...latestData };
  }
  else {
    console.error('서버로부터 데이터를 불러오는 데 실패했습니다.');
  }
  infoLoaded.value = true;
});


// 모든 필드에 대한 편집 상태를 추적하기 위한 객체
const isEditing = reactive({
  email: false, nickname: false, age: false, money: false,
  salary: false, job: false, location: false,
});


// 모든 필드에 대한 편집 가능한 값을 관리하기 위한 객체
const editableFields = reactive({});

// 편집 상태 토글 및 수정 사항 적용
const toggleEdit = (field) => {
  isEditing[field] = !isEditing[field];
  if (isEditing[field]) {
    editableFields[field] = modifiyInfo.value[field];
  } else {
    modifiyInfo.value[field] = editableFields[field];
    info.value[field] = editableFields[field]; // 화면에 바로 반영
  }
};

// 카카오의 우편 번호 서비스 API 사용
const openPostcode = () => {
  new daum.Postcode({
    oncomplete: function (data) {
      // editableFields와 modifiyInfo의 location 필드를 모두 업데이트합니다.
      if (isEditing.location) {
        editableFields.location = data.address;
        modifiyInfo.value.location = data.address;
      }
      else {
        info.value.location = data.address;
        modifiyInfo.value.location = data.address;
      }
    }
  }).open();
};

// 변경 사항을 서버로 전송하는 함수
const submitChanges = () => {
  // console.log(modifiyInfo.value)
  axios({
    method: "put",
    url: `http://127.0.0.1:8000/accounts/myinfo/${info.value.id}/`,
    data: modifiyInfo.value,
    headers: {
      'Authorization': `Token ${store.token}`
    }
  })
    .then((res) => {
      // Object.assign을 사용하여 info.value 업데이트
      Object.assign(info.value, res.data);
      // 필요하다면 store.mydata도 업데이트
      Object.assign(store.mydata, res.data);
      window.alert('변경 사항이 저장 됐습니다.');
    })
    .catch((err) => {
      console.log(err)
    })
};

// 숫자 자릿수3칸마다 , 추가하는 메소드
const formatNumber = (value) => {
  return Number(value).toLocaleString();
};
</script>

<style scoped>
.marg {
  margin: 3%;
}

.color {
  background-color: #3F445C;
  color: #FFF3EB;
  border-radius: 7px;
  margin-left: 5px;
}

.flipcolor { 
  background-color: #FFF3EB;
  color: #3F445C;
}
</style>
