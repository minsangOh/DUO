<template>
  <div class="marg">
    <table>
      <thead>
        <tr>
          <th class="no color">No.</th>
          <th class="title color">제목</th>
          <th class="name color">작성자</th>
          <th class="date color">작성일</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in sortedArticles" :key="article.id" @click="goToArticle(article.id)">
          <td class="no">{{ article.id }}</td>
          <td class="title">{{ article.title }}</td>
          <td class="name">{{ article.author.username }}</td>
          <td class="date">{{ article.created_at }}</td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td colspan="4" class="button-cell">
            <button class="button button--winona button--border-thin button--round-s" data-text="Create New"
              @click="goToCreate">
              <span>Create New</span>
            </button>
          </td>
        </tr>
      </tfoot>
    </table>
  </div>
</template>

<script setup>
import { onBeforeMount, onMounted, computed } from 'vue';
import { useCounterStore } from '@/stores/counter'
import { useRouter } from 'vue-router';

const store = useCounterStore()
const router = useRouter()

onMounted(() => {
  store.getArticles();
});

onBeforeMount(() => {
  store.getArticles()
})

// 게시글을 ID 기준 내림차순으로 정렬
const sortedArticles = computed(() => {
  return store.articles.slice().sort((a, b) => b.id - a.id).map(article => ({
    ...article,
    created_at: formatDate(article.created_at)
  }));
});

// 날짜 포맷 함수
const formatDate = (dateString) => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
};

// 게시글 상세페이지 조회
const goToArticle = (articleId) => {
  router.push({ name: 'detail', params: { id: articleId } });
};

// 게시글 작성 페이지 이동
const goToCreate = () => {
  router.push({ name: 'create' });
};

</script>

<style lang="scss" scoped>
.button-cell {
  text-align: right;
  /* 버튼을 오른쪽 정렬 */
  padding: 10px;
  /* 버튼과 테이블 셀 사이의 여백을 설정 */
}

table {
  width: 90vw;
  text-align: center;
  border: 1px solid #fff;
  border-spacing: 1px;
  font-family: 'Cairo', sans-serif;
  margin: auto;
}

table td {
  padding: 10px;
  background-color: #eee;
}

table th {
  background-color: rgb(40, 124, 250);
  color: #fff;
  padding: 10px;
}

.no {
  width: 5%;
}

.title {
  width: 70%;
  text-align: left;
}

.name {
  width: 10%;
}

.date {
  width: 15%;
}

@media screen and (max-width: 600px) {
  table {
    width: 100%;
  }

  th,
  td {
    padding: 8px;
  }

  .no,
  .title,
  .name,
  .date {
    width: auto;
  }
}

.button--winona {
  position: relative;
  overflow: hidden;
  padding: 2;
  transition: border-color 0.3s, background-color 0.3s;
  transition-timing-function: cubic-bezier(0.2, 1, 0.3, 1);
}

.button--winona::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  /* 수직 중앙 정렬 */
  left: 5px;
  /* 수평 중앙 정렬 */
  transform: translate(-50%, -50%);
  /* 정확한 중앙으로 이동 */
  opacity: 0;
  transition: opacity 0.3s, transform 0.3s;
  transition-delay: 0.3s;
}

.button--winona>span {
  display: block;
  transition: opacity 0.3s, transform 0.3s;
}

.button--winona:not(:hover)>span {
  opacity: 1;
  transform: translate3d(0, 0, 0);
}

.button--winona:hover::after {
  opacity: 1;
  /* 글자가 다시 나타나도록 opacity 변경 */
  transform: translate3d(0, 0, 0);
  transition-delay: 0s;
}

.button--winona:hover>span {
  opacity: 0;
  transform: translate3d(0, -25%, 0);
  transition-delay: 0s;
}

.button--winona:hover {
  border-color: #3f51b5;
}

.button--border-thin {
  border: 1px solid;
}

.button--round-s {
  border-radius: 5px;
}

.marg {
  margin: 3%;
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
