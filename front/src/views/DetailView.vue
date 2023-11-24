<template>
  <div class="article-container">
    <h1 class="article-title">자유게시판</h1>
    <div v-if="article" class="article-details">
      <div class="article-metadata">
        <p><router-link :to="{ name: 'profile', params: { id: article.author.id } }">{{ article.author.username
        }}</router-link></p>
        <p class="article-sub-title"> {{ article.title }}</p>
        <p>{{ formatDate(article.created_at) }}</p>
      </div>
      <div class="article-content">
        <p>{{ article.content }}</p>
        <div v-if="article.author.id === store.mydata.id" class="article-delete-button">
          <button @click="deleteArticle()">게시글 삭제</button>
        </div>
      </div>


      <div v-if="comments.length >= 0" class="article-comments">
        <h4>댓글</h4>
        <div v-for="comment in comments" :key="comment.id" class="comment">
          <strong class="comment-author">
            <router-link :to="{ name: 'profile', params: { id: comment.author.id } }">
              {{ comment.author.username }}
            </router-link>:
          </strong>
          <span class="comment-content" :class="{ 'full-width': comment.author.id !== store.mydata.id }">{{
            comment.content }}</span>
          <span v-if="comment.author.id === store.mydata.id" class="comment-delete" @click="deleteComment(comment.id)"
            title="댓글 삭제">&#10005;</span>
        </div>

        <!-- Comment Form -->
        <div class="comment-form-container">
          <form @submit.prevent="postComment" class="comment-form">
            <input type="text" v-model="newComment" class="comment-form-input" placeholder="댓글을 입력하세요">
            <button type="submit" class="comment-form-submit">댓글 달기</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useCounterStore } from '@/stores/counter'
import { useRoute } from 'vue-router'
import { useRouter } from 'vue-router'

const store = useCounterStore()
const route = useRoute()
const router = useRouter()
const article = ref(null)

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/articles/${route.params.id}/`
  })
    .then((res) => {
      // console.log(res.data)
      article.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
  store.myInfo().then(() => {
    const userId = store.mydata; // mydata는 ref일 수 있으므로 .value 사용
    console.log(userId);
  }).catch(err => {
    console.error("Error fetching user info:", err);
  });
})




const comments = ref([])
const newComment = ref('')
const token = store.token

// 게시글 삭제
const deleteArticle = function () {
  if (window.confirm('Are you sure that you want to delete this article?')) {
    axios({
      method: 'delete',
      url: `${store.API_URL}/articles/${route.params.id}/`,
      headers: {
        'Authorization': `Token ${token}`
      }
    })
      .then(() => {
        console.log('Article deleted successfully');
        store.mutations.removeArticle(route.params.id);
        updateLocalStorage()
        router.push({ name: 'article' });
      })
      .catch((error) => {
        console.error('Error deleting article:', error);
      });
  }
}

function updateLocalStorage() {
  localStorage.setItem('articles', JSON.stringify(store.articles));
}


// 댓글 목록 불러오기
onMounted(() => {
  axios.get(`${store.API_URL}/articles/${route.params.id}/comments/`)
    .then(response => {
      comments.value = response.data;
    });
});

// 댓글 작성
const postComment = () => {
  // console.log(token)
  console.log(`${store.API_URL}/articles/${route.params.id}/comments/`)
  axios({
    method: 'post',
    url: `${store.API_URL}/articles/${route.params.id}/comments/`,
    headers: {
      'Authorization': `Token ${token}`
    },
    data: {
      content: newComment.value,
      article: route.params.id
    }
  })
    .then(response => {
      comments.value.push(response.data);
      newComment.value = '';
    })
    .catch(err => {
      console.error(err);
    });
};

// 댓글 삭제
const deleteComment = (commentId) => {
  axios({
    method: 'delete',
    url: `${store.API_URL}/articles/comments/delete/${commentId}/`, // 백엔드의 댓글 삭제 URL
    headers: {
      'Authorization': `Token ${token}`
    }
  })
    .then(() => {
      // 댓글 목록에서 삭제된 댓글 제거
      comments.value = comments.value.filter(comment => comment.id !== commentId);
    })
    .catch(err => {
      console.error(err);
    });
};

// 날짜 포맷 함수
const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};
</script>


<style lang="scss" scoped>
// $primary-color: #0d6efd;
$primary-color: #3F445C;
$secondary-color: #6c757d;
$background-color: #f8f9fa;
$border-color: #dee2e6;

.article-container {
  padding: 2rem;
  background-color: $background-color;
  border: 1px solid $border-color;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 0.125rem 0.25rem rgba($border-color, 0.075);
}

.article-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: $primary-color;
  margin-bottom: 1rem;
}

.article-sub-title {
  font-weight: bold;
  font-size: 1.2rem;
  color: black;
}

.article-comments {
  background-color: #fff;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid $border-color;
  border-radius: 0.375rem;
}

.article-metadata {
  display: flex;
  justify-content: space-between;
  font-size: 0.875rem;
  color: $secondary-color;

  p {
    margin-bottom: 0; // Remove margin for a tight metadata display
  }
}

.comment {
  display: flex;
  align-items: center;
  justify-content: flex-start; // 모든 자식 요소를 컨테이너의 시작 지점으로 정렬

  .comment-author {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .comment-content {
    flex-grow: 1;
    margin-right: auto; // 삭제 버튼이 없을 때도 오른쪽 공간을 확보
  }


  .comment-delete {
    flex-grow: 0; // 삭제 버튼은 필요한 만큼의 공간만 차지하도록 설정
    margin-left: auto; // 삭제 버튼을 오른쪽으로 정렬
    padding: 0.25rem 0.5rem;
    font-size: 0.75rem;
    color: $secondary-color;
    background-color: transparent;
    border: none;
    cursor: pointer;

    &:hover {
      color: #dc3545;
      background-color: $background-color;
    }
  }
}


// Form styles
.comment-form {
  display: flex;
  gap: 1rem;
  align-items: center;

  &-input {
    flex-grow: 1;
    border: 1px solid #ced4da;
    padding: 0.5rem;
    border-radius: 0.375rem;
  }

  &-submit {
    padding: 0.5rem 1rem;
    border-radius: 0.375rem;
    border: 1px solid $primary-color;
    background-color: $primary-color;
    color: #fff;

    &:hover {
      background-color: darken($primary-color, 5%);
    }
  }
}

.article-comments {
  background-color: #fff;
  padding: 1rem;
  border: 1px solid $border-color;
  border-radius: 0.375rem;
  margin-bottom: 1rem;

  // 댓글 제목
  h4 {
    color: $primary-color;
    margin-bottom: 1rem;
  }

  // 댓글 작성 폼 스타일
  .comment-form-container {
    border-top: 1px solid $border-color;
    padding-top: 1rem;
    margin-top: 1rem;
  }

  // 폼 스타일
  .comment-form {
    display: flex;
    gap: 1rem;
    align-items: center;

    &-input {
      flex-grow: 1;
      border: 1px solid #ced4da;
      padding: 0.5rem;
      border-radius: 0.375rem;
    }

    &-submit {
      padding: 0.5rem 1rem;
      border-radius: 0.375rem;
      border: 1px solid $primary-color;
      background-color: $primary-color;
      color: #fff;

      &:hover {
        background-color: darken($primary-color, 5%);
      }
    }
  }
}

.article-delete-button {
  text-align: right; // 우측 정렬
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  color: $secondary-color;
  background-color: transparent;
  border: none;
  cursor: pointer;

  button {
    padding: 0.25rem 0.5rem;
    color: $secondary-color;
    background-color: transparent;
    border: none;
    cursor: pointer;

    &:hover {
      color: #dc3545;
      background-color: $background-color;
    }
  }
}

.comment-delete {
  padding: 0.25rem 0.5rem; // 패딩을 줄여서 버튼 크기를 작게 만듭니다.
  font-size: 0.75rem; // 폰트 사이즈를 줄여서 덜 눈에 띄게 만듭니다.
  color: $secondary-color; // 버튼의 색상을 부드러운 회색으로 변경합니다.
  border: none; // 테두리를 제거합니다.
  background-color: transparent; // 배경색을 투명하게 만듭니다.
  cursor: pointer; // 마우스 오버시 커서를 변경합니다.

  &:hover {
    color: #dc3545; // 마우스 오버시 색상을 변경하여 사용자에게 인터랙션이 가능함을 알립니다.
    background-color: $background-color; // 마우스 오버시 배경색을 약간 변경합니다.
  }

}
</style>
