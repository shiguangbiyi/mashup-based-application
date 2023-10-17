<template>
  <div>
    <div class="video-background">
      <video autoplay muted loop id="myVideo">
      <source src="../assets/city.mp4" type="video/mp4">
        Your browser does not support HTML5 video.
      </video>
    </div>
    <div class="header">
        世界城市信息检索系统
    </div>
    <div class="search-container">
      <input type="text" class="search-box" placeholder="搜索城市..." v-model="cityName">
      <button class="search-button" @click="getSummary">搜索</button>
      <p>{{ summary }}</p>
    </div>
    <div id="container"></div>
  </div>

</template>

<script setup>
import { onMounted,ref } from 'vue';
import axios from 'axios';
const summary = ref('');
const cityName = ref('');
const getSummary = async () => {
  try {
    const response = await axios.get('http://localhost:5000/get_summary', {
      params: {
        keyword: cityName.value
      }
    });
    summary.value = response.data.summary;

  } catch (error) {
    console.log("出错")
    console.error(error);
  }
};

onMounted(()=>{
  const BMap = window.BMap;
  var map = new BMap.Map("container");
  map.centerAndZoom(new BMap.Point(116.404, 39.915), 11);
	var local = new BMap.LocalSearch(map, {
		renderOptions:{map: map}
	});
	local.search(cityName);
})



</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

#container {
  width: 300px;
  height: 300px;
  position: fixed;
  left: 0px; /* 调整这里来改变地图到右侧的距离 */
  bottom: 20px; /* 调整这里来改变地图到底部的距离 */
  z-index: 1;
}

/* 其他CSS规则保持不变 */
.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
}

#myVideo {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.header {
  color: #e0e0e0;
  padding: 40px;
  text-align: center;
  font-size: 40px;
  font-weight: bold;
  margin-top: 160px;
  text-transform: uppercase;
  font-family: '等线', Arial, sans-serif;
}
.search-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 20px;
}

.search-box {
  padding: 10px;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  width: 400px;
  height: 20px;
  background-color: #f2f2f2;
  outline: none;
  text-indent: 15px;
  font-family: 'Arial', sans-serif;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) inset;
}

.search-button {
  background-color: #3498db;
  color: #ffffff;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  padding: 10px 20px;
  margin-left: 10px;
  cursor: pointer;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #207cca;
}

</style>
