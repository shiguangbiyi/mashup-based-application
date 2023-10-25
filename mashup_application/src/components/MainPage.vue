<template>
  <div>
    <div class="video-background" >
      <video autoplay muted loop id="myVideo">
        <source src="../assets/city.mp4" type="video/mp4">
        Your browser does not support HTML5 video.
      </video>
    </div>
    <div v-if="isSearched" class="headerandsearch-up">
      <div class="header-up">
        世界城市信息检索系统
      </div>
      <div class="search-up">
        <input type="text" class="search-box" placeholder="搜索城市...支持中文搜索，大部城市支持英文搜索" list="cities" @input="handleSearch" v-model="cityName">
        <datalist id="cities" class="datalist">
          <option v-for="(city, index) in cityList" :value="city" :key="index" class="option">
            {{ city }}
          </option>
        </datalist>
        <button class="search-button" @click="getResult">搜索</button>
      </div>
    </div>
    <div v-else>
      <div class="header">
        世界城市信息检索系统
      </div>
      <div class="search">
        <input type="text" class="search-box" placeholder="搜索城市...支持中文搜索，大部城市支持英文搜索" list="cities" @input="handleSearch" v-model="cityName">
        <datalist id="cities" class="datalist">
          <option v-for="(city, index) in cityList" :value="city" :key="index" class="option">
            {{ city }}
          </option>
        </datalist>
        <button class="search-button" @click="getResult">搜索</button>
      </div>
    </div>

    <div class="summary-container" style="margin-top: 100px;" v-if="isSearched">
      <div class="summary-card">
        <div v-if="imglist && imglist.length > 0" class="image-row">
          <div class="image-col" v-for="(img, imgIndex) in imglist.slice(0, 6)" :key="imgIndex">
            <img :src="img.src" :alt="img.alt" class="image-item" />
          </div>
        </div>
        <div v-else class="no-image-message">抱歉，本城市暂无图片资源</div>
        <span class="source-label">来自unsplash</span>
        <!-- <div v-if="imglistBaidu && imglistBaidu.length > 0" class="image-row">
          <div class="image-col" v-for="(img, imgIndex) in imglistBaidu.slice(0, 6)" :key="imgIndex">
            <img :src="img.src" :alt="img.alt" class="image-item" />
          </div>
        </div>
        <div v-else class="no-image-message">抱歉，本城市暂无图片资源</div>
        <span class="source-label">来自百度图片</span> -->
        <button class="card-button" @click="redirectToUnsplash()">查看更多</button>
      </div>
    </div>

    <div class="summary-container" v-if="summary1 || summary2">
      <div class="summary-card">
        <h2 class="card-title">基本资料</h2>
        <p v-if="summary2 !== '没有找到相关词条的简述。' && summary2.length >= 10" class="card-content">{{ summary2 }}</p>
        <span v-if="summary2 !== '没有找到相关词条的简述。' && summary2.length >= 10" class="source-label">来自维基百科</span>
        <button v-if="summary2 !== '没有找到相关词条的简述。' && summary2.length >= 10" class="card-button" @click="redirectToWiki()">查阅详情</button>
        <p v-if="summary1 !== '没有找到相关词条的简述。'" class="card-content">{{ summary1 }}</p>
        <span v-if="summary1 !== '没有找到相关词条的简述。'" class="source-label">来自百度百科</span>
        <button v-if="summary1 !== '没有找到相关词条的简述。'" class="card-button" @click="redirectToBaidu()">查阅详情</button>
        <p v-if="!summary1 && !summary2" class="card-content">百度百科数据获取不稳定，请打开VPN查阅维基百科</p>
      </div>
    </div>


    <div class="economic-container" v-if="WorldBankdata[0]">
      <div class="summary-card">
        <h2 class="card-title">经济/环境</h2>
        <div class="link-list">
          <a v-for="(item, index) in WorldBankdata" :key="index" :href="item.url" target="_blank" class="link-item">
            {{ item.title }}
            <hr class="divider">
          </a>
        </div>
        <span class="source-label">来自世界银行</span>
      </div>
    </div>

    <div class="economic-container" v-if="isSearched">
      <div class="summary-card">
        <h2 class="card-title">相关新闻</h2>
        <hr class="divider">
        <div class="link-list" v-if="newslist.data">
          <a v-for="(item, index) in newslist.data" :key="index" :href="item.url" target="_blank" class="link-item">
            {{ item.title }}
            <hr class="divider">
          </a>
          <span class="source-label">来自mediastack</span>
        </div>
        <hr class="divider">
        <div class="link-list" v-if="newslistWangYi.length!=0">
          <a v-for="(item, index) in newslistWangYi.data" :key="index" :href="item.url" target="_blank" class="link-item">
            {{ item.title }}
            <hr class="divider">
          </a>
          <span class="source-label">来自网易新闻</span>
        </div>

      </div>
    </div>

    <div class="weather-map">
      <div v-if="isSearched" class="weather">
        <div class="weather-details">
          <div class="weather-icon">
            <svg v-if="firstPart==='晴'" t="1698226527625" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="11702" width="100" height="100"><path d="M522.666667 362.666667c76.458667 0 138.666667 62.208 138.666666 138.666666S599.125333 640 522.666667 640 384 577.792 384 501.333333s62.208-138.666667 138.666667-138.666666m0-64c-111.936 0-202.666667 90.730667-202.666667 202.666666s90.730667 202.666667 202.666667 202.666667 202.666667-90.730667 202.666666-202.666667-90.730667-202.666667-202.666666-202.666666zM522.666667 256c-17.6 0-32-14.4-32-32v-85.333333c0-17.6 14.4-32 32-32s32 14.4 32 32v85.333333c0 17.6-14.4 32-32 32z" fill="#F9A825" p-id="11703"></path><path d="M522.666667 896c-17.6 0-32-14.4-32-32v-85.333333c0-17.6 14.4-32 32-32s32 14.4 32 32v85.333333c0 17.6-14.4 32-32 32z" fill="#FBB03B" p-id="11704"></path><path d="M696.554667 327.850667a32.106667 32.106667 0 0 1 0-45.248l60.330666-60.330667a32.106667 32.106667 0 0 1 45.248 0 32.106667 32.106667 0 0 1 0 45.248l-60.330666 60.330667a32.064 32.064 0 0 1-45.248 0zM244.010667 780.394667a32.106667 32.106667 0 0 1 0-45.248l60.330666-60.330667a32.106667 32.106667 0 0 1 45.248 0 32.106667 32.106667 0 0 1 0 45.248l-60.330666 60.330667a32.064 32.064 0 0 1-45.248 0zM349.184 327.850667a32.106667 32.106667 0 0 1-45.248 0l-60.330667-60.330667a32.106667 32.106667 0 0 1 0-45.248 32.106667 32.106667 0 0 1 45.248 0l60.330667 60.330667a32.064 32.064 0 0 1 0 45.248zM801.728 780.394667a32.106667 32.106667 0 0 1-45.248 0l-60.330667-60.330667a32.106667 32.106667 0 0 1 0-45.248 32.106667 32.106667 0 0 1 45.248 0l60.330667 60.330667a32.064 32.064 0 0 1 0 45.248zM277.333333 501.333333c0 17.6-14.4 32-32 32h-85.333333c-17.6 0-32-14.4-32-32S142.4 469.333333 160 469.333333h85.333333c17.6 0 32 14.4 32 32zM917.333333 501.333333c0 17.6-14.4 32-32 32h-85.333333c-17.6 0-32-14.4-32-32s14.4-32 32-32h85.333333c17.6 0 32 14.4 32 32z" fill="#F9A825" p-id="11705"></path></svg>
          </div>
          <div class="weather-info">
            <p class="temperature">{{ weatherData.temp }}℃</p>
            <p class="other-info">
              湿度:{{ weatherData.humidity }}% | 气压:{{ weatherData.pressure }}hPa
            </p>
            <p class="other-info">日出时间:{{ weatherData.sunrise }}</p>
            <p class="other-info">日落时间:{{ weatherData.sunset }}</p>
            <p class="description">{{ weatherData.description }}</p>
            <p class="wind-info">风速:{{ weatherData.wind }}m/s | 风向:{{ weatherData.wind_deg }}</p>
            <p class="cloudiness">云量:{{ weatherData.cloudiness }}%</p>
          </div>
        </div>
      </div>
      <div id="container"></div>
    </div>
  </div>
</template>

<script setup>
import { ref,reactive } from 'vue';
import axios from 'axios';
const summary1 = ref('');
const summary2 = ref('');
const cityName = ref('');
const isSearched = ref(false);
const weatherData = reactive({
  temp: ref(''),
  temp_max: ref(''),
  temp_min: ref(''),
  humidity: ref(''),
  pressure: ref(''),
  sunrise: ref(''),
  sunset: ref(''),
  wind: ref(''),
  wind_deg: ref(''),
  cloudiness: ref(''),
  description: ref('')
});


// 处理输入的部分，根据输入给出城市列表提示，使用了teleportAPI
const cityList = ref([]);
const fetchData = async (searchTerm) => {
  try {
    const response = await axios.get(`https://api.teleport.org/api/cities/?search=${searchTerm}`);
    cityList.value = response.data?._embedded?.['city:search-results']?.map((result) => result.matching_full_name) || [];
  } catch (error) {
    console.error(error);
  }
};
const handleSearch = () => {
  if(cityName.value !== '')
    fetchData(cityName.value);
};


// 处理输入框中的默认输入，将中文输入和英文输入分开，以便进行不同API调用
const cityEnglish = ref('')
const cityChinese = ref('')
const divide = () => {
  const parts = cityName.value.split(',');
  cityEnglish.value = parts[0].trim();
  if (parts.length > 1) {
    const regex = /\(([^)]+)\)/;
    const matches = cityName.value.match(regex);
    cityChinese.value = matches ? matches[1] : '';
  } else {
    cityChinese.value = '';
  }
};
const setDefaultCityName = () => {
  const name = cityName.value.trim();
  const isChineseOrEnglish = /^[\u4E00-\u9FA5]+$|^[\u4E00-\u9FA5\w]+$/g.test(name);
  if (isChineseOrEnglish && cityList.value.length > 0) {
    cityName.value = cityList.value[0];
  }
};


// 图片展示1，来自unsplashAPI
const imglist = ref([])
const fetchPic = async () => {
  imglist.value = [];
  try {
    const response = await axios.get(`https://api.unsplash.com/search/photos?page=1&query=${cityEnglish.value}&client_id=KaE2Y3RZ-mL65vgGnU52BYdj9tychGSsq86twcaY1ls`);
    const results = response.data.results;
    results.forEach(result => {
      const imgInfo = {
        src: result.urls.regular,
        alt: result.alt_description
      };
      imglist.value.push(imgInfo);
    });
  } catch (error) {
    console.log("请求图片信息时出错")
    console.error(error);
  }
};
function redirectToUnsplash() {
  const url = `https://unsplash.com/s/photos/${cityEnglish.value}`;
  window.open(url, '_blank');
}
// 图片展示2，来自百度图片
// const imglistBaidu = ref([])
// const fetchPicBaidu = async () => {
//   try {
//     const response = await axios.get('http://localhost:5003/search_images', {
//       params: {
//         keyword: cityChinese.value
//       }
//     });
//     const results = response.data;
//     results.forEach((result) => {
//       const imgInfo = {
//         src: result.thumbURL,
//         alt: result.fromPageTitle,
//       };
//       imglist.value.push(imgInfo);
//     });
//   } catch (error) {
//     console.log('请求百度图片信息时出错');
//     console.error(error);
//   }
// };


// 获取城市天气，来自openWeatherAPI，使用后端进行整合，使用英文搜索
let firstPart = ''
const getWeather = async () => {
  try {
    const response = await axios.get('http://localhost:5001/translate', {
      params: {
        keyword: cityEnglish.value
      }
    });
    weatherData.temp = response.data.temp;
    weatherData.temp_max = response.data.temp_max;
    weatherData.temp_min = response.data.temp_min;
    weatherData.humidity = response.data.humidity;
    weatherData.pressure = response.data.pressure;
    weatherData.sunrise = response.data.sunrise;
    weatherData.sunset = response.data.sunset;
    weatherData.wind = response.data.wind;
    weatherData.wind_deg = response.data.wind_deg;
    weatherData.cloudiness = response.data.cloudiness;
    weatherData.description = response.data.description;
    const description = weatherData.description;
    firstPart = description.split('，')[0].trim();
    setWeatherIcon();
  } catch (error) {
    console.log("请求天气信息时出错")
    console.error(error);
  }
}
const weatherIcon = ref('');
const setWeatherIcon = () => {
  console.log(firstPart)
  switch (firstPart) {
    case '晴':
      weatherIcon.value = 'https://bpic.588ku.com/element_origin_min_pic/19/04/29/57a2f8e3f552085fdc10a6bfb4ddeeb3.jpg';
      console.log(weatherIcon.value)
      break;
    case '多云':
      weatherIcon.value = 'cloudy-icon.png';
      console.log(weatherIcon.value)
      break;
    case 'rainy':
      weatherIcon.value = 'rainy-icon.png';
      break;
    default:
      console.log(firstPart)
      weatherIcon.value = 'default-icon.png';
      break;
  }
};


// 调用百度地图API，使用中文搜索
const loadmap = async () => {
  const BMap = window.BMap;
  var map = new BMap.Map("container");
  map.centerAndZoom(new BMap.Point(116.404, 39.915), 11);
  map.enableScrollWheelZoom(true);
	var local = new BMap.LocalSearch(map, {
		renderOptions:{map: map}
	});
  if(cityChinese.value){
    local.search(cityChinese.value);
  }else{
    local.search(cityEnglish.value);
  }
}


// 调用世界银行API，使用后端对数据进行处理，使用英文搜索
const WorldBankdata = ref([]);
const fetchWorldBankData = async () => {
  try {
    const response = await axios.get('http://localhost:5002/get_worldbank_data', {
      params: {
        keyword: cityEnglish.value
      }
    });
    WorldBankdata.value = response.data;
  } catch (error) {
    console.log("请求世界银行信息时出错")
    console.error(error);
  }
};


// 调用维基百科API和百度百科API，使用后端进行数据获取并整合
const getSummary = async () => {
  let params = {};

  if (cityChinese.value) {
    params = {
      keyword: cityChinese.value
    };
  } else {
    params = {
      keyword: cityEnglish.value
    };
  }
  try {
    const response = await axios.get('http://localhost:5000/get_summary', {params});
    summary1.value = response.data.summary1;
    summary2.value = response.data.summary2;
  } catch (error) {
    console.log("请求百科信息时出错")
    console.error(error);
  }
}
function redirectToWiki() {
  const url = `https://zh.wikipedia.org/wiki/${cityChinese.value}`;
  window.open(url, '_blank');
}
function redirectToBaidu() {
  const url = `https://baike.baidu.com/item/${cityChinese.value}`;
  window.open(url, '_blank');
}

// 调取mediastackAPI，获取新闻信息
const newslist = ref([])
const newslistWangYi = ref([])
const getnews = async() => {
  try {
    const response = await axios.get('http://api.mediastack.com/v1/news?access_key=c83a02c3414b168ce6a33859d59cb233&keywords=' + cityEnglish.value);
    newslist.value = response.data
    console.log(newslist.value)
  } catch (error) {
    console.log("请求新闻列表时出错")
    console.error(error);
  }
}
const getnewsWangYi = async() => {
  try {
    const response = await axios.get('http://localhost:5004/get_news', {
      params: {
        keyword: cityChinese.value
      }
    });
    newslistWangYi.value=response
    console.log(newslistWangYi.value)
  } catch (error) {
    console.log("请求网易新闻列表时出错")
    console.error(error);
  }
}

const getResult = async () => {
  setDefaultCityName();
  if (cityName.value === '' || cityList.value.length === 0) {
      if(!(cityName.value === cityList.value[0])){
          alert('搜索结果不存在，请输入正确的城市名称');
          return
      }
  }
  isSearched.value = true;
  divide();
  fetchPic();
  // fetchPicBaidu();
  getSummary();
  loadmap();
  getWeather();
  getnews();
  getnewsWangYi();
  fetchWorldBankData();
};

</script>

<style scoped>
.weather-map {
  width: 25%;
  position: fixed;
  right: 0;
  top: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
}

.datalist {
  position: absolute;
  z-index: 1;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 5px;
  max-height: 200px;
  overflow-y: auto;
}

.option {
  padding: 10px;
  cursor: pointer;
}

.option:hover {
  background-color: #ddd;
}
.image-unit {
  display: flex;
  flex-wrap: wrap;
  margin-top: 20px;
  margin-left: 30px;
  width: 70%;
}

.image-row {
  display: flex;
  width: 100%;
  justify-content: space-between;
}

.image-col {
  width: 30%;
  margin-bottom: 20px;
}

.image-item {
  width: 100%;
  height: 200px; /* 根据需要设置统一的高度 */
  object-fit: cover;
}

.divider {
  margin: 10px 0; /* 调整分割线的上下边距 */
  border: 0; /* 移除默认的边框样式 */
  border-top: 1px solid #ccc; /* 定义分割线样式 */
}
#more-button {
  margin-top: 20px;
}
.weather {
  width: 300px;
  height: 300px;
  color: #000000;
  background: linear-gradient(135deg, #51bcf6, #e0e0e0);
  position: absolute;
  top: 3%;
  left: 50%;
  transform: translate(-50%, -0%);
}
#container {
  width: 300px;
  height: 300px;
  z-index: 1;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, 5%);
}

.video-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
  background-color: #666467;
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
.header-up {
  position: fixed;
  color: #000000;
  top: 0;
  left: 0;
  padding: 0px;
  margin-top: 25px;
  margin-left: 50px;
  text-align: left;
  font-size: 30px;
  width: 100%;
  z-index: 1;
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
.search-up {
  position: fixed;
  top: 3%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1;
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

.headerandsearch-up {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%; /* 让顶栏宽度充满屏幕 */
  height: 80px; /* 你可以根据需要调整高度 */
  background-color: #ffffff;
  display: flex;
  align-items: center; /* 让内容垂直居中 */
  justify-content: space-between; /* 可以根据需要调整内容的水平布局 */
  padding: 0 20px; /* 可以根据需要调整内边距 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 可以根据需要添加阴影效果 */
  z-index: 1000; /* 确保顶栏在其他元素之上 */
  clip-path: polygon(0 0, 71% 0, 71% 100%, 0 100%);
  border-top-left-radius: 10px; /* 左上角圆角半径 */
  border-bottom-right-radius: 10px; /* 左下角圆角半径 */
  /* 其他样式 */
}
.search-button:hover {
  background-color: #207cca;
}
.summary-container {
  display: flex;
  margin-top: 20px;
  margin-left: 30px;
}

.economic-container {
  display: flex;
  margin-top: 20px;
  margin-left: 30px;
}

.summary-card {
  background-color: #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: left;
  width: 70%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.card-button {
  background-color: #239cf9;
  color: #ffffff;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  margin-left: auto;
  margin-top: 10px;
  cursor: pointer;
}

.source-label {
  font-size: 12px;
  color: #888888;
  margin-top: 5px;
}
.card-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333333;
}
.link-list {
  display: flex;
  flex-direction: column;
  margin-top: 10px;
}

.link-item {
  text-decoration: none;
  color: #239cf9;
  padding: 5px 0;
  transition: color 0.3s;
}

.link-item:hover {
  color: #207cca;
}

.weather {
  display: flex;
  justify-content: center;
  align-items: center;
}

.weather-details {
  display: flex;
  align-items: center;
}

.weather-icon {
  margin-right: 20px;
}

.weather-icon img {
  width: 60px;
  height: 60px;
}

.temperature {
  font-size: 28px;
  font-weight: bold;
  margin: 0;
}

.other-info {
  font-size: 14px;
  margin: 5px 0;
}

.description {
  font-size: 18px;
  margin: 10px 0;
}

.wind-info {
  font-size: 14px;
  margin: 5px 0;
}

.cloudiness {
  font-size: 14px;
  margin: 5px 0;
}
</style>
