import axios from "axios";
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import { useCounterStore } from "./counter";

export const useFinanceStore = defineStore('finance', () => {
  const API_URL = "http://127.0.0.1:8000/apis/";
  const router = useRouter();
  const cstore = useCounterStore()


  // 정기예금 불러오기
  const depositList = ref(null);
  const getDepositProducts = function() {
    axios({
      method: 'get',
      url: `${API_URL}deposit-products/`,
    }).then(res => {
        console.log('deposit lists', res.data);
        depositList.value = res.data;
      })
      .catch(err => {
        console.log('Error fetching deposit products:', err);
      });
  };
  
  // 정기적금 불러오기
  const saveList = ref(null);
  const getSaveProducts = function() {
    axios({
      method: 'get',
      url: `${API_URL}save-products/`,
    }).then(res => {
        console.log('save lists', res.data);
        saveList.value = res.data;
      })
      .catch(err => {
        console.log('Error fetching save products:', err);
      });
  };

  // 정기예금 상세
  const deposit = ref(null);
  const getDeposit = function(fin_prdt_cd) {
    axios({
      method: 'get',
      url: `${API_URL}deposit-detail/${fin_prdt_cd}/`,
    }) .then(res => {
      console.log('deposit detail', res.data);
      deposit.value = res.data;
    }) .catch(err => {
      console.log('Error fetching deposit detail: ', err);
    })
  };

  // 정기적금 상세
  const save = ref(null);
  const getSave = function(fin_prdt_cd) {
    axios({
      method: 'get',
      url: `${API_URL}save-detail/${fin_prdt_cd}/`,
    }) .then(res => {
      console.log('save detail', res.data);
      save.value = res.data;
    }) .catch(err => {
      console.log('Error fetching save detail: ', err);
    })
  };

  // 정기예금 이자 리스트
  const depositOptions = ref([])
  const getDepositOptions = function() {
    axios({
      method: 'get',
      url: `${API_URL}deposit-product-options/`,
    }) .then(res => {
      console.log('deposit options', res.data);
      depositOptions.value = res.data;
    }) .catch(err => {
      console.log('Error fetching deposit options: ', err);
    })
  }

  // 정기적금 이자 리스트
  const saveOptions = ref([])
  const getSaveOptions = function() {
    axios({
      method: 'get',
      url: `${API_URL}save-product-options/`,
    }) .then(res => {
      console.log('save options', res.data);
      saveOptions.value = res.data;
    }) .catch(err => {
      console.log('Error fetching save options: ', err);
    })
  }


  const joinSave = ref([])
  const joinDeposit = ref([])

  const getJoinSave = function(saveId) {
    axios({
      method: 'get',
      url: `${API_URL}joinsave/${saveId}`,
      headers: {
        Authorization: `Token ${cstore.token}`,
        'Content-Type': 'application/json',
      },
    }) .then(res => {
      console.log('joinSave:', res.data)
      joinSave.value = res.data;
    }) .catch(err => {
      console.log('Error fetching join save', err)
    })
  }
  const getJoinDeposit = function(depositId) {
    axios({
      method: 'get',
      url: `${API_URL}joindeposit/${depositId}`,
      headers: {
        Authorization: `Token ${cstore.token}`,
        'Content-Type': 'application/json',
      },
    }) .then(res => {
      console.log('joinDeposit:', res.data)
      joinDeposit.value = res.data;
    }) .catch(err => {
      console.log('Error fetching join deposit', err)
    })
  }

  // 정기예금 가입/취소
  const joinOrUnjoinDeposit = async (depositId, method) => {
    try {
      console.log(cstore)
      const response = await axios({
        method,
        url: `${API_URL}joindeposit/${depositId}/`,
        headers: {
          Authorization: `Token ${cstore.token}`,
          'Content-Type': 'application/json',
        },
      });

      depositList.value = response.data;

      return response.data; 
    } catch (error) {
      console.error('Error during join/unjoin deposit:', error);
      throw error; 
    }
  };

  // 정기적금 가입/취소
  const joinOrUnjoinSave = async (saveId, method) => {
    try {
      console.log('API URL:', `${API_URL}join-save/${saveId}/`);
      console.log('Authorization Token:', cstore.token);
      console.log('Data:', { save_id: saveId });

      const response = await axios({
        method,
        url: `${API_URL}joinsave/${saveId}/`,
        headers: {
          Authorization: `Token ${cstore.token}`,
          'Content-Type': 'application/json',
        },
        data: { save: saveId },
      });

      saveList.value = response.data;

      return response.data; 
    } catch (error) {
      console.error('Error during join/unjoin save:', error);
      throw error;
    }
  };

  return{ 
    API_URL, depositList, saveList, deposit, save, depositOptions, saveOptions, joinSave, joinDeposit,
    getDepositProducts, getSaveProducts, getDeposit, getSave, getDepositOptions, getSaveOptions,
    joinOrUnjoinDeposit, joinOrUnjoinSave, getJoinSave, getJoinDeposit,
  }
}, { persist: true });
