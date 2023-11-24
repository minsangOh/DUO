<template>
  <div class="container marg">
    <h1>Map</h1>
    <select class="me-3" v-model="selectedState">
      <option v-for="state in states" :key="state">{{ state }}</option>
    </select>
    <select class="me-3" v-model="selectedCounty">
      <option v-for="county in countries" :key="county">{{ county }}</option>
    </select>
    <select class="me-3" v-model="selectedBank">
      <option v-for="bank in banks" :key="bank">{{ bank }}</option>
    </select>

    <button @click="findBanks" class="btn btn-secondary color">찾기</button>
    <div class="mt-4 map" ref="map"></div>
  </div>
</template>

<script>
import data from "@/data/data.json";
/* global kakao */
export default {
  data() {
    return {
      map: {},
      infowindow: {},
      ps: {},
      markers: [],
      mapSelectInfo: [],
      banks: [],
      selectedState: "광역시/도를 선택하세요",
      selectedCounty: "시군구를 선택하세요",
      selectedBank: "국민은행",
    };
  },
  computed: {
    states() {
      return this.mapSelectInfo.map((el) => el.name);
    },
    countries() {
      // 딱 하나의 엘리먼트만 추출될 것
      // ex) 경기도에 해당하는 시군구, 부산광역시에 해당하는 시군구
      // filter 의 리턴값은 배열이므로,
      // 배열 안에 하나의 객체만 있으니 [0] 으로 깔끔하게 객체만 받아오는것임
      const result = this.mapSelectInfo.filter(
        (el) => el.name === this.selectedState
      )[0];
      return result.countries;
    },
  },
  created() {
    // 그냥 받을 경우, 주소 참조가 되어버려 created 작동 시점에도 데이터 남아있음
    // 따라서, 값만 받아오기 위해 JSON.parse, JSON.stringify 사용
    const dataCopy = JSON.parse(JSON.stringify(data));
    // 각각의 시군구 맨 앞에 "시군구를 선택하세요" 넣음
    this.mapSelectInfo = dataCopy.mapInfo.map((el) => {
      el.countries.unshift("시군구를 선택하세요");
      return el;
    });
    // 맨 앞에 넣을 객체 하나
    this.mapSelectInfo.unshift({
      name: "광역시/도를 선택하세요",
      countries: ["시군구를 선택하세요"],
    });
    // 은행 배열은 그냥 가져옴
    this.banks = dataCopy.bankInfo;
  },
  mounted() {
    //지도를 담을 영역의 DOM 가져옴
    const container = this.$refs.map;
    const options = {
      //지도를 생성할 때 필요한 기본 옵션
      //지도의 중심좌표. 위도(latitude), 경도(longitude)
      center: new kakao.maps.LatLng(37.49818, 127.027386),
      //지도의 레벨(확대, 축소 정도)
      level: 3,
    };
    // 지도 생성 및 객체 리턴
    this.map = new kakao.maps.Map(container, options);
    // 인포윈도우 객체
    this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    // 검색을 위한 Places 객체
    this.ps = new kakao.maps.services.Places();
  },
  methods: {
    // 지도에 표시된 모든 마커를 지움
    clearMarkers() {
      this.markers.forEach((marker) => {
        // 마커 지움
        marker.setMap(null);
      });
      // 마커 추적을 위한 상태 초기화
      this.markers = [];
    },
  // 상위카테고리가 바뀔때마다 작동됨
    // 하위카테고리가 텅 비어있는 모습 방지
    resetChildSelect() {
      this.selectedCounty = "시군구를 선택하세요";
    },
    displayMarker(place) {
      // 마커 세팅
      const marker = new kakao.maps.Marker({
        map: this.map,
        position: new kakao.maps.LatLng(place.y, place.x),
      });

      // 마커에 클릭 이벤트 추가
      kakao.maps.event.addListener(marker, "click", () => {
        //  Kakao Maps directions link
        const directionsLink = `https://map.kakao.com/link/to/${place.place_name},${place.y},${place.x}`;
        const content =
        `<div style="padding:10px;font-size:14px;max-width:200px;">${place.place_name}` +
        `<a href="${directionsLink}" target="_blank">길찾기</a>` +
        `</div>`;

        // Set content and open the info window
        this.infowindow.setContent(content);
        this.infowindow.open(this.map, marker);
      });

      // 마커 추적을 위해 리턴
      return marker;
    },
    findBanks() {
      // 사용자가 선택 안했을 경우를 대비한 에러처리
      if (
        this.selectedState === "광역시/도를 선택하세요" ||
        this.selectedCounty === "시군구를 선택하세요"
      ) {
        return;
      }
      // 기존 마커 지우고 시작
      this.clearMarkers();
      // 검색어 입력해서 카카오로 보냄
      this.ps.keywordSearch(
        `${this.selectedState} ${this.selectedCounty} ${this.selectedBank}`,
        (data, status) => {
          if (status === kakao.maps.services.Status.OK) {
            // 현재 지도 넓이를 미리 받아둠
            const bounds = new kakao.maps.LatLngBounds();
            // data 는 배열로서, 카카오맵 검색결과로 받아온 데이터를 의미
            data.forEach((el) => {
              // displayMarker 는 직접 정의함
              // 마커를 두는 함수
              const marker = this.displayMarker(el);
              // 마커 추적을 위한 상태 배열에 저장
              this.markers.push(marker);
              // 해당 마커의 좌표를 포함하도록 영역정보 확장
              bounds.extend(new kakao.maps.LatLng(el.y, el.x));
            });
            // 마커들을 전부 포함하도록 지도의 사이즈 재설정
            this.map.setBounds(bounds);
          }
        }
      );
    },
  },
};
</script>

<style scoped>
.map {
  width: 500px;
  height: 400px;
}

.marg {
  margin: 3%;
}

.color {
  background-color: #3F445C;
  color: #FFF3EB;
}
</style>






<!-- <template>
  <div class="container marg">
    <h1>Map</h1>
    <select class="me-3" v-model="selectedState" @change="resetChildSelect">
      <option v-for="state in states" :key="state">{{ state }}</option>
    </select>
    <select class="me-3" v-model="selectedCounty">
      <option v-for="county in countries" :key="county">{{ county }}</option>
    </select>
    <select class="me-3" v-model="selectedBank">
      <option v-for="bank in banks" :key="bank">{{ bank }}</option>
    </select>

    <button @click="findBanks" class="btn btn-secondary color">찾기</button>
    <div class="mt-4 map" ref="map"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import data from "@/data/data.json";
/* global kakao */

export default {
  setup() {
    const selectedState = ref("광역시/도를 선택하세요");
    const selectedCounty = ref("시군구를 선택하세요");
    const selectedBank = ref("국민은행");
    const map = ref({});
    const infowindow = ref({});
    const ps = ref({});
    const markers = ref([]);
    const mapSelectInfo = ref([]);
    const banks = ref([]);

    const states = computed(() => mapSelectInfo.value.map((el) => el.name));
    const countries = computed(() => {
      const result = mapSelectInfo.value.filter(
        (el) => el.name === selectedState.value
      )[0];
      return result.countries;
    });

    const clearMarkers = () => {
      markers.value.forEach((marker) => {
        marker.setMap(null);
      });
      markers.value = [];
    };

    const resetChildSelect = () => {
      selectedCounty.value = "시군구를 선택하세요";
    };

    const displayMarker = (place) => {
      const marker = new kakao.maps.Marker({
        map: map.value,
        position: new kakao.maps.LatLng(place.y, place.x),
      });

      kakao.maps.event.addListener(marker, "click", () => {
        const directionsLink = `https://map.kakao.com/link/to/${place.place_name},${place.y},${place.x}`;
        const content =
          `<div style="padding:10px;font-size:14px;max-width:200px;">${place.place_name}` +
          `<a href="${directionsLink}" target="_blank">길찾기</a>` +
          `</div>`;

        infowindow.value.setContent(content);
        infowindow.value.open(map.value, marker);
      });

      markers.value.push(marker);

      return marker;
    };

    const findBanks = () => {
      if (
        selectedState.value === "광역시/도를 선택하세요" ||
        selectedCounty.value === "시군구를 선택하세요"
      ) {
        return;
      }

      clearMarkers();

      ps.value.keywordSearch(
        `${selectedState.value} ${selectedCounty.value} ${selectedBank.value}`,
        (data, status) => {
          if (status === kakao.maps.services.Status.OK) {
            const bounds = new kakao.maps.LatLngBounds();
            data.forEach((el) => {
              const marker = displayMarker(el);
              markers.value.push(marker);
              bounds.extend(new kakao.maps.LatLng(el.y, el.x));
            });
            map.value.setBounds(bounds);
          }
        }
      );
    };

    return {
      selectedState,
      selectedCounty,
      selectedBank,
      states,
      countries,
      banks,
      findBanks,
      resetChildSelect,
      map,
      infowindow,
      ps,
      markers,
      mapSelectInfo,
    };
  },
  onMounted() {
    const dataCopy = JSON.parse(JSON.stringify(data));
    this.mapSelectInfo = dataCopy.mapInfo.map((el) => {
      el.countries.unshift("시군구를 선택하세요");
      return el;
    });
    this.mapSelectInfo.unshift({
      name: "광역시/도를 선택하세요",
      countries: ["시군구를 선택하세요"],
    });
    this.banks = dataCopy.bankInfo;

    const container = this.$refs.map;
    const options = {
      center: new kakao.maps.LatLng(37.49818, 127.027386),
      level: 3,
    };

    this.map = new kakao.maps.Map(container, options);
    this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
    this.ps = new kakao.maps.services.Places();
  },
};
</script>

<style scoped>
.map {
  width: 500px;
  height: 400px;
}

.marg {
  margin: 3%;
}

.color {
  background-color: #3F445C;
  color: #FFF3EB;
}
</style> -->
