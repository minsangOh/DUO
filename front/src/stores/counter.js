import axios from "axios";
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";

export const useCounterStore = defineStore('counter', () => {

  const API_URL = "http://127.0.0.1:8000";
  const token = ref(null);
  const router = useRouter();
  const mydata = ref(null)
  const articles = ref([]);

  const mutations = {
    removeArticle(id) {
      articles.value = articles.value.filter(article => article.id !== id);
    }
  };

  

  // 게시글
  const getArticles = function () {
    axios({
      method: "get",
      url: `${API_URL}/articles/list/`,
      headers: {
        'Authorization': `Token ${token.value}`
      }
    })
      .then((res) => {
        // console.log(res.data)
        articles.value = res.data;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  // 회원가입
  const signUp = function (payload) {
    const { username, first_name, last_name, email, password1, password2, nickname, age, money, salary, job, location, } = payload;

    axios({
      method: "post",
      url: `${API_URL}/accounts/signup/`,
      data: { username, first_name, last_name, email, password1, password2, nickname, age, money, salary, job, location, },
    })
      .then((res) => {
        console.log(res);
        window.alert('회원가입이 완료 됐습니다.')
        // router.push({ name: 'loginMain' })
        window.location.reload();
      })
      .catch((err) => {
        console.log(err);
        window.alert('비밀번호가 맞는지 확인하시고, 모든 필드가 입력됐는지 확인하세요.')
      });
  };

  // 로그인
  const logIn = function (payload) {
    let { username, password } = payload;
    return axios({
      method: "post",
      url: `${API_URL}/accounts/login/`,
      data: {
        username,
        password
      },
    })
      .then((res) => {
        token.value = res.data.key;
        myInfo()
        router.push({ name: "home" });
        window.alert('로그인에 성공했습니다.')

      })
      .catch((err) => {
        // 로그인 실패 시 출력
        window.alert('아이디 또는 비밀번호를 잘못 입력 하셨습니다. 다시 확인하세요')
        username = null
        password = null
      });
  };

  // 로그아웃
  const logOut = function () {
    token.value = null
    router.push({ name: "home" });
    window.alert('로그아웃에 성공했습니다.')
  }

  // 내 정보
  const myInfo = function () {
    // Promise를 반환하도록 수정
    return new Promise((resolve, reject) => {
      axios({
        method: "get",
        url: `${API_URL}/accounts/myinfo/`,
        headers: {
          'Authorization': `Token ${token.value}`
        },
      })
      .then((res) => {
        mydata.value = res.data;
        resolve(res.data); // 성공 시, 데이터를 resolve로 반환
      }) 
      .catch((err) => {
        console.log(err);
        reject(err); // 에러 발생 시, 에러를 reject로 반환
      });
    });
  };
  
  // 로그인 여부 확인
  const isLogin = computed(() => {
    if (token.value === null) {
      return false;
    } else {
      return true;
    }
  });

  // 회원탈퇴
  const deleteAccount = function (confirmPassword) {
    axios({
      method: "delete",
      url: `${API_URL}/accounts/delete/`,
      headers: {
        'Authorization': `Token ${token.value}`
      },
      data: confirmPassword
    })
      .then(response => {
        console.log(response);
        window.alert('회원탈퇴가 성공했습니다.')
        token.value = null
        router.push({ name: "home" });
      })
      .catch(err => {
        console.error(err);
        throw err; // 에러를 상위 컴포넌트로 전달
      });
  };



  return {
    API_URL, articles, isLogin, token, mydata,
    getArticles, signUp, logIn, logOut, myInfo, deleteAccount, mutations
  }
}, { persist: true })
