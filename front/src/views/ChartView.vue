<template>
  <div class="marg">
    <h2>예금 및 적금 금리 비교</h2>
    <div v-if="saveGraphic || depositGraphic">
      <img v-if="saveGraphic" :src="'data:image/png;base64,' + saveGraphic" alt="적금 그래프" />
      <img v-if="depositGraphic" :src="'data:image/png;base64,' + depositGraphic" alt="예금 그래프" />
    </div>
    <div v-else>
      <p>그래프를 불러오는 중...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      saveGraphic: null,
      depositGraphic: null,
    };
  },
  created() {
    this.fetchGraphData();
  },
  methods: {
    fetchGraphData() {
      const userId = this.$route.params.id;
      axios.get(`http://127.0.0.1:8000/accounts/graph/${userId}/`)
        .then(response => {
          this.saveGraphic = response.data.save_graphic;
          this.depositGraphic = response.data.deposit_graphic;
        })
        .catch(error => {
          console.error("그래프 데이터를 가져오는 중 오류가 발생했습니다:", error);
        });
    },
  }
};
</script>

<style scoped>
.marg {
  margin: 3%;
}

img {
  width:100%;
}
</style>
