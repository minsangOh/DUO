import axios from "axios";
import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useTopStore = defineStore('top', () => {
  const API_URL = "http://127.0.0.1:8000/accounts/";

  // 정기예금 불러오기
  const top3deposits = ref(null);
  const depositjob = ref(null);
  const depositlocation = ref(null);

  const getTopDeposits = function() {
    axios({
      method: 'get',
      url: `${API_URL}top3deposits/`,
    }).then(res => {
      top3deposits.value = res.data;
      depositjob.value = res.data.top_job_products;
      depositlocation.value = res.data.top_location_products;
    }).catch(err => {
      console.error('Error fetching deposit products:', err);
    });
  };

  const top3DFormatted = computed(() => {
    return top3deposits.value;
  });

  // 정기적금 불러오기
  const top3saves = ref(null);
  const savejob = ref(null);
  const savelocation = ref(null);

  const getTopSaves = function() {
    axios({
      method: 'get',
      url: `${API_URL}top3saves/`,
    }).then(res => {
      top3saves.value = res.data;
      savejob.value = res.data.top_job_products;
      savelocation.value = res.data.top_location_products;
    }).catch(err => {
      console.error('Error fetching save products:', err);
    });
  };

  const top3SFormatted = computed(() => {
    return top3saves.value;
  });

  return { 
    depositlocation, depositjob, top3DFormatted, savelocation, savejob, top3SFormatted,
    getTopDeposits, getTopSaves,
  };  
}, { persist: true });
