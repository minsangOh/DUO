<template>
  <header>
    <nav class="navbar navbar-expand-lg bg-navcolor">
      <div class="container-fluid">
        <RouterLink to="/" class="link">진상DUO</RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="bi bi-list"
              viewBox="0 0 16 16">
              <path fill-rule="evenodd"
                d="M2 13.5a.5.5 0 0 1 .5-.5H13.5a.5.5 0 0 1 0 1H2.5a.5.5 0 0 1-.5-.5zm0-5a.5.5 0 0 1 .5-.5H13.5a.5.5 0 0 1 0 1H2.5a.5.5 0 0 1-.5-.5zm0-5a.5.5 0 0 1 .5-.5H13.5a.5.5 0 0 1 0 1H2.5a.5.5 0 0 1-.5-.5z" />
            </svg>
          </span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0 d-flex align-items-center">
            <li class="nav-item mr-5">
              <RouterLink to="/finance" class="link">예적금 비교</RouterLink>
            </li>
            <li class="nav-item mr-5">
              <RouterLink to="/exim" class="link">환율 계산기</RouterLink>
            </li>
            <li class="nav-item mr-5">
              <RouterLink to="/map" class="link">은행 지도</RouterLink>
            </li>
            <li class="nav-item mr-5">
              <RouterLink :to="{ name: 'article' }" class="link">자유게시판</RouterLink>
            </li>
            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle link" href="#" id="navbarDropdown" role="button"
                data-bs-toggle="dropdown" aria-expanded="false">
                상품관리
              </a>
              <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                <!-- 로그인을 진행하지 않았을 때 출력-->
                <div>
                  <li>
                    <RouterLink :to="{ name: 'jobdeposit' }" class="dropdown-item">직업별 인기 예금</RouterLink>
                  </li>
                  <li>
                    <RouterLink :to="{ name: 'jobsave' }" class="dropdown-item">직업별 인기 적금</RouterLink>
                  </li>
                  <li>
                    <hr class="dropdown-divider">
                  </li>
                  <li>
                    <RouterLink :to="{ name: 'locationdeposit' }" class="dropdown-item">지역별 인기 예금</RouterLink>
                  </li>
                  <li>
                    <RouterLink :to="{ name: 'locationsave' }" class="dropdown-item">지역별 인기 적금</RouterLink>
                  </li>
                </div>
                <!-- 로그인 상태일 때 출력 -->
                <div v-if="store.token !== null">
                  <li>
                    <hr class="dropdown-divider">
                  </li>
                  <RouterLink :to="{ name: 'chart', params: { id: store.mydata.id } }" class="dropdown-item">나의 상품 금리
                  </RouterLink>
                </div>
              </ul>
            </li>


            <li class="nav-item dropdown">
              <a class="nav-link dropdown-toggle link" href="#" id="navbarDropdown" role="button"
                data-bs-toggle="dropdown" aria-expanded="false">
                USER관리
              </a>
              <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
                <!-- 로그인을 진행하지 않았을 때 출력-->
                <div v-if="store.token === null">
                  <li>
                    <RouterLink :to="{ name: 'loginMain' }" class="dropdown-item">로그인, 회원가입</RouterLink>
                  </li>
                </div>
                <!-- 로그인 상태일 때 출력 -->
                <div v-else>
                  <RouterLink :to="{ name: 'myprofile' }" class="dropdown-item">내 프로필</RouterLink>
                  <li>
                    <hr class="dropdown-divider">
                  </li>
                  <li><button class="dropdown-item" @click="logOut">로그아웃</button></li>
                  <RouterLink :to="{ name: 'deleteaccount' }" class="dropdown-item">회원탈퇴</RouterLink>
                </div>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <RouterView />
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useCounterStore } from '@/stores/counter'

const store = useCounterStore()
const logOut = function () {
  store.logOut()
}
</script>


<style scoped>
.link {
  text-decoration: none;
  color: #FFF3EB
}

.nav-item {
  margin-left: 1rem;
}

.bg-navcolor {
  background-color: #3F445C
}

.navbar-toggler-icon {
  color: #FFF3EB;
  border-color: #FFF3EB;
  border-width: 10px;
  font-weight: bold;
}
</style>
