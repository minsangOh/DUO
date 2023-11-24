<template>
  <div class="container my-5">
    <form @submit.prevent="createArticle" class="border p-4 rounded">
      <div class="mb-3">
        <label for="title" class="form-label">제목을 입력하세요</label>
        <input type="text" v-model.trim="title" id="title" class="form-control">
      </div>
      <div class="mb-3">
        <label for="content" class="form-label">당신의 이야기를 적어보세요...</label>
        <textarea v-model.trim="content" id="content" class="form-control" rows="5"></textarea>
      </div>
      <input type="submit" class="btn color">
    </form>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router'

const title = ref(null)
const content = ref(null)
const store = useCounterStore()
const router = useRouter()

const createArticle = function () {
  axios({
    method: 'post',
    url: `${store.API_URL}/articles/list/`,
    data: {
      title: title.value,
      content: content.value
    },
    headers: {Authorization:`Token ${store.token}`},
  })
    .then((res) => {
      // console.log(res)
      router.push({ name: 'article' })
    })
    .catch((err) => {
      console.log(err)
    })
}

</script>

<style lang="scss" scoped>
// 폼의 커스텀 스타일
.container {
  max-width: 700px; // 필요에 따라 폭 조정
}

form {
  background-color: #f8f9fa; // 연한 회색 배경
  border: 1px solid #dee2e6; // Bootstrap 기본 연한 회색 테두리
  
  // 라벨 스타일링
  .form-label {
    font-weight: bold; // 글씨 굵게
  }

  // 입력창 및 텍스트 영역 스타일링
  .form-control {
    border-radius: 0.25rem; // 입력창과 텍스트 영역의 둥근 모서리
    border: 1px solid #ced4da; // Bootstrap의 기본 테두리 색상

    &:focus {
      border-color: #a1cbef; // 포커스 상태의 연한 파란색 테두리
      box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25); // Bootstrap 기본 포커스 그림자
    }
  }

  // 제출 버튼 스타일링
  .btn-primary {
    padding: 0.375rem 0.75rem; // 버튼의 기본 패딩
    font-size: 1rem; // 기본 글씨 크기
    line-height: 1.5; // 기본 줄 간격
    border-radius: 0.25rem; // 다른 입력창과 일치하는 모서리
    background-color: #0d6efd; // Bootstrap의 기본 파란색 버튼
    border: 1px solid #0d6efd; // 배경색과 일치하는 테두리
    
    &:hover {
      background-color: #0b5ed7; // 마우스를 올렸을 때 더 진한 파란색으로 변경
      border-color: #0a58ca; // 마우스를 올렸을 때 테두리 색상도 변경
    }
  }
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