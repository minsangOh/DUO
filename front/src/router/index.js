import { createRouter, createWebHistory } from "vue-router";
import HomeView from "@/views/HomeView.vue";
import DeleteAccount from "@/components/DeleteAccount.vue";
// import LogInView from "@/components/LogInView.vue";
import LogInMainView from "@/views/LogInMain.vue";
import ChartView from "@/views/ChartView.vue";
import MyProfileView from "@/views/MyProfileView.vue";
import ProfileView from "@/views/ProfileView.vue";
import { useCounterStore } from '../stores/counter';
import MapView from '@/views/MapView.vue';
import EximView from '@/views/EximView.vue';
import Finance from '@/components/Finance.vue';
import DepositProductsView from '@/views/DepositProductsView.vue';
import SaveProductsView from '@/views/SaveProductsView.vue';
import DepositDetailView from '@/views/DepositDetailView.vue';
import SaveDetailView from '@/views/SaveDetailView.vue';

import ArticleView from '@/views/ArticleView.vue'
import DetailView from '@/views/DetailView.vue'
import CreateView from '@/views/CreateView.vue'

import JobDepositView from '@/views/JobDepositView.vue'
import LocationDepositView from '@/views/LocationDepositView.vue'
import JobSaveView from '@/views/JobSaveView.vue'
import LocationSaveView from '@/views/LocationSaveView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { // 메인 페이지
      path: "/",
      name: "home",
      component: HomeView,
    },
    { // 로그인 메인
      path: "/loginMain",
      name: "loginMain",
      component: LogInMainView,
    },
    { // 회원탈퇴
      path: "/deleteaccount",
      name: "deleteaccount",
      component: DeleteAccount,
    },
    { // 게시판
      path: '/article',
      name: 'article',
      component: ArticleView
    },
    { // 내 상품 비교
      path: '/chart/:id',
      name: 'chart',
      component: ChartView
    },
    { // 게시글 조회
      path: '/articles/:id',
      name: 'detail',
      component: DetailView
    },
    { // 게시글 생성
      path: '/create',
      name: 'create',
      component: CreateView
    },
    { // 내 프로필 조회
      // path: "/myprofile/:id",
      path: "/myprofile",
      name: "myprofile",
      component: MyProfileView,
    },
    // { // 내 프로필 수정
    //   // path: "/myprofile/:id",
    //   name: "/myprofile",
    //   component: MyProfileView,
    // },
    { // 다른 유저 프로필 조회
      path: "/profile/:id",
      name: "profile",
      component: ProfileView,
    },
    { // 카카오 지도 
      path: '/map',
      name: 'map',
      component: MapView
    },
    { // 환율 
      path: '/exim',
      name: 'exim',
      component: EximView
    },
    {  // 예적금 정보
      path: '/finance',
      component: Finance,
      children: [
        { // 예금
          path: '/deposit',
          name: 'deposit',
          component: DepositProductsView
        },
        { // 적금
          path: '/save',
          name: 'save',
          component: SaveProductsView
        },
      ],
    },
    { // 예금 상세정보
      path: '/depositdetail/:fin_prdt_cd',
      name: 'depositdetail',
      component: DepositDetailView,
      props: true
    },
    { // 적금 상세정보
      path: '/savedetail/:fin_prdt_cd',
      name: 'savedetail',
      component: SaveDetailView,
      props: true
    },
    { // 지역별 top3 예금
      path: '/locationdeposit',
      name: 'locationdeposit',
      component: LocationDepositView,
    },
    { // 직업별 top3 예금
      path: '/jobdeposit',
      name: 'jobdeposit',
      component: JobDepositView,
    },
    { // 지역별 top3 적금
      path: '/locationsave',
      name: 'locationsave',
      component: LocationSaveView,
    },
    { // 직업별 top3 적금
      path: '/jobsave',
      name: 'jobsave',
      component: JobSaveView,
    },
  ],
});


router.beforeEach((to, from) => {
  const store = useCounterStore()
  if (to.name === 'article' && !store.isLogin) {
    window.alert('로그인이 필요합니다.')
    return { name: 'login' }
  }
  if ((to.name === 'signup' || to.name === 'login') && (store.isLogin)) {
    window.alert('이미 로그인 했습니다..')
    return { name: 'home' }
  }
})


export default router
