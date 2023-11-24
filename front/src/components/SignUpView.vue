<template>
  <section class="auth-container">
    <div class="left">
      <div class="sign-up">
        <form @submit.prevent="signUp">
          <p><label for="username">아이디: </label>
            <input type="text" id="username" v-model.trim="username" />
          </p>
          <p><label for="first_name">성: </label>
            <input type="text" id="first_name" v-model.trim="first_name" />
          </p>
          <p><label for="last_name">이름: </label>
            <input type="text" id="last_name" v-model.trim="last_name" />
          </p>
          <p><label for="email">이메일: </label>
            <input type="email" id="email" v-model.trim="email" />
          </p>
          <p><label for="password1">비밀번호: </label>
            <input type="password" id="password1" v-model.trim="password1" />
          </p>
          <p><label for="password2">비밀번호 확인: </label>
            <input type="password" id="password2" v-model.trim="password2" />
          </p>
          <p><label for="nickname">닉네임: </label>
            <input type="text" id="nickname" v-model.trim="nickname" />
          </p>
          <p><label for="age">나이: </label>
            <input type="number" id="age" v-model.trim="age" />
          </p>
          <p><label for="money">현재 자산: </label>
            <input type="number" id="money" v-model.trim="money" />
          </p>
          <p><label for="salary">월 수입: </label>
            <input type="number" id="salary" v-model.trim="salary" />
          </p>
          <p>
            <label for="job">직업: </label>
            <select id="job" v-model.trim="job">
              <option value="">Select Job</option>
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
          </p>
          <p><label for="location">주소: </label>
            <input type="text" id="location" v-model="location" @click="openPostcode" />
          </p>
          <input type="submit" value="Sign Up" @click.prevent="signUpEvent" />
        </form>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router';
import { defineEmits } from 'vue';
const emit = defineEmits(['change-view']);

const store = useCounterStore()
const route = useRouter()
const username = ref(null)
const first_name = ref(null)
const last_name = ref(null)
const email = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const nickname = ref(null)
const age = ref(null)
const money = ref(null)
const salary = ref(null)
const job = ref(null)
const location = ref(null)
// const financial_products_deposit = ref(null)
// const financial_products_save = ref(null)

const openPostcode = () => {
  new daum.Postcode({
    oncomplete: function (data) {
      location.value = data.address;
    }
  }).open();
};


const signUpEvent = function () {
  const payload = {
    username: username.value,
    first_name: first_name.value,
    last_name: last_name.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    age: age.value,
    money: money.value,
    salary: salary.value,
    job: job.value,
    location: location.value,
  }
  store.signUp(payload);
};


</script>

<style>
.sign-up {
  max-height: 300px;
  /* 스크롤 영역의 최대 높이 설정 */
  overflow-y: scroll;
  /* 세로 스크롤바 활성화 */
}

.sign-up label,
.sign-up input {
  display: block;
  /* 블록 레벨 요소로 만들어 줄바꿈이 일어나도록 함 */
  margin-left: 0;
  /* 왼쪽 여백을 없앰 */
  text-align: left;
  /* 텍스트를 왼쪽으로 정렬 */
  width: 100%;
  /* 부모 컨테이너의 전체 너비를 차지하도록 함 */
}

.sign-up label {
  margin-bottom: .5rem;
  /* 라벨 아래에 약간의 여백을 추가 */
  font-weight: bold;
  /* 라벨 텍스트를 굵게 함 */
}

.sign-up input {
  margin-bottom: 1rem;
  /* 인풋 아래에 여백을 추가 */
  padding: .5rem;
  /* 인풋 내부에 패딩을 추가 */
  border: 1px solid #ccc;
  /* 인풋에 테두리를 추가 */
}

.sign-up form {
  padding: 1rem;
  /* 폼 내부에 패딩을 추가 */
}

/* "Sign Up" 버튼과 "Sign In" 링크의 스타일을 추가할 수도 있습니다 */
.sign-up input[type="submit"] {
  background-color: #26c6da;
  /* 배경색 설정 */
  color: white;
  /* 텍스트 색상 설정 */
  border: none;
  /* 테두리 제거 */
  padding: .5rem 1rem;
  /* 패딩 설정 */
  margin-top: 1rem;
  /* 위쪽 여백 설정 */
  cursor: pointer;
  /* 마우스 포인터를 손가락 모양으로 변경 */
  border-radius: .25rem;
  /* 모서리 둥글게 설정 */
}

.sign-up a {
  color: #26c6da;
  /* 링크 색상 설정 */
  text-decoration: none;
  /* 밑줄 제거 */
}

.sign-up select {
  margin-bottom: 1rem; /* 드롭다운 아래에 여백을 추가 */
  padding: .5rem; /* 드롭다운 내부에 패딩을 추가 */
  border: 1px solid #ccc; /* 드롭다운에 테두리를 추가 */
  width: 100%; /* 부모 컨테이너의 전체 너비를 차지하도록 함 */
  border-radius: .25rem; /* 모서리를 둥글게 설정 */
  background-color: white; /* 배경색을 설정 */
  color: black; /* 텍스트 색상을 설정 */
}
</style>