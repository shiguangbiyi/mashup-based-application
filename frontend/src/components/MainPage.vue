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
        <input type="text" class="search-box" placeholder="搜索城市...支持中文搜索" list="cities" @input="handleSearch" v-model="cityName">
        <datalist id="cities" class="datalist">
          <option v-for="(city, index) in cityList" :value="city" :key="index" class="option" @click="getResult">
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
        <input type="text" class="search-box" placeholder="搜索城市...支持中文搜索" list="cities" @input="handleSearch" v-model="cityName">
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
        <h2 class="card-title">视觉/印象</h2>
        <div v-if="imglist && imglist.length > 0" class="image-row">
          <div class="image-col" v-for="(img, imgIndex) in imglist.slice(0, 6)" :key="imgIndex">
            <img :src="img.src" :alt="img.alt" class="image-item" />
          </div>
        </div>
        <div v-else class="no-image-message">抱歉，本城市暂无图片资源</div>
        <span class="source-label">来自unsplash</span>
        <button class="card-button" @click="redirectToUnsplash()">查看更多</button>

        <div v-if="imglistBing.data" class="image-row">
          <div class="image-col" v-for="(url, index) in imglistBing.data" :key="index">
            <img :src="url" alt="city image" class="image-item">
          </div>
        </div>
        <div v-else class="no-image-message">抱歉，本城市暂无图片资源</div>
        <span class="source-label">来自必应图片</span>
        <button class="card-button" @click="redirectToBing()">查看更多</button>
      </div>
    </div>

    <div class="summary-container" v-if="sougouBaseInfo.data!='数据获取异常'&&sougouBaseInfo.data">
      <div class="summary-card">
        <h2 class="card-title">基本信息</h2>
        <div class="info-container" v-for="(value, key) in sougouBaseInfo.data" :key="key">
          <div class="info-item">
            <p class="key">{{ key }}:</p>
          </div>
          <div class="info-item">
            <p class="value">{{ value }}</p>
          </div>
          <hr class="info-divider" v-if="!$last">
        </div>
        <span class="source-label">来自搜狗百科</span>
      </div>
    </div>
    
    <div class="summary-container" v-if="summary1 || summary2">
      <div class="summary-card">
        <h2 class="card-title">基本资料</h2>
        <div class="project-report">以下是关于{{ cityChinese }}的基本资料，信息来源包括维基百科、百度百科、搜狗百科。</div>
        <p v-if="summary2 !== '没有找到相关词条的简述。' && summary2.length >= 10" class="card-content">{{ summary2 }}</p>
        <span v-if="summary2 !== '没有找到相关词条的简述。' && summary2.length >= 10" class="source-label">来自维基百科</span>
        <button v-if="summary2 !== '没有找到相关词条的简述。' && summary2.length >= 10" class="card-button" @click="redirectToWiki()">查阅详情</button>
        <p v-if="summary1 !== '没有找到相关词条的简述。'" class="card-content">{{ summary1 }}</p>
        <span v-if="summary1 !== '没有找到相关词条的简述。'" class="source-label">来自百度百科</span>
        <button v-if="summary1 !== '没有找到相关词条的简述。'" class="card-button" @click="redirectToBaidu()">查阅详情</button>
        <p v-if="summary3 !== '没有找到相关词条的简述。'" class="card-content">{{ summary3 }}</p>
        <span v-if="summary3 !== '没有找到相关词条的简述。'" class="source-label">来自搜狗百科</span>
        <button v-if="summary3 !== '没有找到相关词条的简述。'" class="card-button" @click="redirectToSougou()">查阅详情</button>
      </div>
    </div>


    <div class="economic-container" v-if="WorldBankdata[0]">
      <div class="summary-card">
        <h2 class="card-title">经济/环境</h2>
        <div class="project-report">以下是关于{{ cityChinese }}的经济和环境相关项目的报告内容，包含城市重大项目实施、资金使用情况、目标完成情况以及项目对当地环境改善的影响等方面的数据。信息来源为世界银行。</div>
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
        <div class="project-report">以下是关于{{ cityChinese }}的相关新闻，信息来源包括mediastack、网易新闻。mediastack包含世界大多主流媒体的最新新闻信息，具有较强权威性。另外，网易新闻仅支持国内城市新闻搜索。</div>
        <hr class="divider">
        <div class="link-list" v-if="newslist.data">
          <a v-for="(item, index) in newslist.data" :key="index" :href="item.url" target="_blank" class="link-item">
            {{ item.title }}
            <hr class="divider">
          </a>
          <span class="source-label">来自mediastack</span>
        </div>
        <hr class="divider">
        <div class="link-list" v-if="newslistWangYi">
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
            <svg v-if="firstPart==='多云'" t="1698248648809" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="4974" width="100" height="100"><path d="M742.4 409.6c-6.528 0-14.208 1.024-21.632 2.304C694.016 320.128 610.048 256 512 256c-98.048 0-182.016 64.128-208.768 155.904-7.424-1.28-15.104-2.304-21.632-2.304-77.696 0-140.8 63.104-140.8 140.8s63.104 140.8 140.8 140.8h460.8c77.696 0 140.8-63.104 140.8-140.8s-63.104-140.8-140.8-140.8z m0 230.4H281.6c-49.408 0-89.6-40.192-89.6-89.6s40.192-89.6 89.6-89.6c3.584 0 9.216 0.896 15.232 2.048V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-41.344C361.856 365.056 430.464 307.2 512 307.2s150.272 57.984 163.968 137.984V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-23.552c6.016-1.152 11.776-2.048 15.232-2.048 49.408 0 89.6 40.192 89.6 89.6s-40.192 89.6-89.6 89.6z" fill="#FF8B00" p-id="4975"></path></svg>
            <svg v-if="firstPart==='阴'" t="1698249075594" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="12596" width="100" height="100"><path d="M826.368 437.632A179.584 179.584 0 0 0 844.8 358.4c0-98.816-80.384-179.2-179.2-179.2-58.88 0-113.792 29.184-147.2 77.056-2.176 0-4.224-0.256-6.4-0.256-98.048 0-182.016 64.128-208.768 155.904-7.424-1.28-15.104-2.304-21.632-2.304-77.696 0-140.8 63.104-140.8 140.8s63.104 140.8 140.8 140.8h460.8c77.696 0 140.8-63.104 140.8-140.8 0-46.208-22.4-87.168-56.832-112.768zM665.6 230.4c70.528 0 128 57.472 128 128 0 19.84-4.608 39.04-13.312 56.576-12.032-3.456-24.704-5.376-37.888-5.376-6.528 0-14.208 1.024-21.632 2.304a215.872 215.872 0 0 0-143.488-145.92A128.384 128.384 0 0 1 665.6 230.4z m76.8 409.6H281.6c-49.408 0-89.6-40.192-89.6-89.6s40.192-89.6 89.6-89.6c3.584 0 9.216 0.896 15.232 2.048V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-41.216A165.7088 165.7088 0 0 1 512 307.2c81.536 0 150.272 57.984 163.968 138.112V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-23.552c6.016-1.152 11.776-2.048 15.232-2.048 49.408 0 89.6 40.192 89.6 89.6s-40.192 89.6-89.6 89.6zM665.6 128c14.08 0 25.6-11.52 25.6-25.6V51.2c0-14.08-11.52-25.6-25.6-25.6s-25.6 11.52-25.6 25.6v51.2c0 14.08 11.52 25.6 25.6 25.6zM972.8 332.8h-51.2c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h51.2c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6zM846.592 203.008c6.528 0 13.056-2.56 18.048-7.552l36.224-36.224c9.984-9.984 9.984-26.24 0-36.224-9.984-9.984-26.24-9.984-36.224 0l-36.224 36.224c-9.984 9.984-9.984 26.24 0 36.224 5.12 4.992 11.648 7.552 18.176 7.552zM466.432 195.456c4.992 4.992 11.52 7.552 18.048 7.552a25.6512 25.6512 0 0 0 18.048-43.776l-36.224-36.224c-9.984-9.984-26.24-9.984-36.224 0-9.984 9.984-9.984 26.24 0 36.224l36.352 36.224z" fill="#FF8B00" p-id="12597"></path></svg>
            <svg v-if="firstPart==='小雨'" t="1698249406153" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14486" width="100" height="100"><path d="M492.544 572.16C484.096 582.016 409.6 670.976 409.6 742.4c0 26.368 9.088 51.2 25.728 69.888 13.184 14.848 37.248 32.512 76.8 32.64 67.2 0 102.4-51.456 102.4-102.4 0-71.424-74.496-160.384-82.944-170.24-9.856-11.52-29.312-11.52-39.04-0.128zM512 793.6v25.6-25.6c-16.512 0-29.44-5.248-38.528-15.36-8.064-9.216-12.672-22.144-12.672-35.84 0-33.408 28.544-80.64 51.2-112 22.656 31.36 51.2 78.592 51.2 112 0 23.552-13.44 51.2-51.2 51.2z" fill="#FF8B00" p-id="14487"></path><path d="M742.4 409.6c-6.528 0-14.208 1.024-21.632 2.304C694.016 320.128 610.048 256 512 256c-98.048 0-182.016 64.128-208.768 155.904-7.424-1.28-15.104-2.304-21.632-2.304-77.696 0-140.8 63.104-140.8 140.8s63.104 140.8 140.8 140.8h76.8c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6h-76.8c-49.408 0-89.6-40.192-89.6-89.6s40.192-89.6 89.6-89.6c3.584 0 9.216 0.896 15.232 2.048V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-41.216A165.7088 165.7088 0 0 1 512 307.2c81.536 0 150.272 57.984 163.968 138.112V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-23.552c6.016-1.152 11.776-2.048 15.232-2.048 49.408 0 89.6 40.192 89.6 89.6s-40.192 89.6-89.6 89.6h-76.8c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h76.8c77.696 0 140.8-63.104 140.8-140.8s-63.104-140.8-140.8-140.8z" fill="#FF8B00" p-id="14488"></path></svg>
            <svg v-if="firstPart==='烟雾'" t="1698249604934" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="14630" width="100" height="100"><path d="M396.8 384h153.6c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6H396.8c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6zM243.2 460.8h307.2c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6H243.2c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6zM166.4 537.6h307.2c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6H166.4a25.6 25.6 0 1 0 0 51.2zM921.6 588.8c0-14.08-11.52-25.6-25.6-25.6H128c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h768c14.08 0 25.6-11.52 25.6-25.6zM896 640H166.4c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h729.6c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6zM396.8 716.8H243.2c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h153.6c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6zM640 460.8h102.4c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6h-102.4c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6zM524.8 512c0 14.08 11.52 25.6 25.6 25.6h268.8c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6H550.4c-14.08 0-25.6 11.52-25.6 25.6zM819.2 716.8H473.6c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h345.6c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6z" fill="#FF8B00" p-id="14631"></path></svg>
            <svg v-if="firstPart==='薄雾'" t="1698249702404" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="15651" width="100" height="100"><path d="M204.8 230.4h537.6c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6H204.8c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6zM742.4 281.6H243.2c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h499.2c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6zM691.2 409.6c0-14.08-11.52-25.6-25.6-25.6H204.8c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h460.8c14.08 0 25.6-11.52 25.6-25.6zM742.4 486.4H320c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h422.4c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6zM665.6 588.8H435.2c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h230.4c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6zM588.8 691.2H435.2c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h153.6c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6zM512 793.6h-76.8c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h76.8c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6z" fill="#FF8B00" p-id="15652"></path></svg>
            <svg v-if="firstPart==='阵雨'" t="1698252031429" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="16663" width="100" height="100"><path d="M512 896c-14.08 0-25.6 11.52-25.6 25.6v51.2c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-51.2c0-14.08-11.52-25.6-25.6-25.6z m-45.568-700.544c4.992 4.992 11.52 7.552 18.048 7.552s13.056-2.56 18.048-7.552c9.984-9.984 9.984-26.24 0-36.224l-36.224-36.224c-9.984-9.984-26.24-9.984-36.224 0-9.984 9.984-9.984 26.24 0 36.224l36.352 36.224zM665.6 128c14.08 0 25.6-11.52 25.6-25.6V51.2c0-14.08-11.52-25.6-25.6-25.6s-25.6 11.52-25.6 25.6v51.2c0 14.08 11.52 25.6 25.6 25.6z m180.992 75.008c6.528 0 13.056-2.56 18.048-7.552l36.224-36.224c9.984-9.984 9.984-26.24 0-36.224-9.984-9.984-26.24-9.984-36.224 0l-36.224 36.224c-9.984 9.984-9.984 26.24 0 36.224 5.12 4.992 11.648 7.552 18.176 7.552zM396.8 819.2c-14.08 0-25.6 11.52-25.6 25.6v51.2c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-51.2c0-14.08-11.52-25.6-25.6-25.6z m576-486.4h-51.2c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6h51.2c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6zM512 742.4c-14.08 0-25.6 11.52-25.6 25.6v51.2c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-51.2c0-14.08-11.52-25.6-25.6-25.6z m314.368-304.768A179.584 179.584 0 0 0 844.8 358.4c0-98.816-80.384-179.2-179.2-179.2-58.88 0-113.792 29.184-147.2 77.056-2.176 0-4.224-0.256-6.4-0.256-98.048 0-182.016 64.128-208.768 155.904-7.424-1.28-15.104-2.304-21.632-2.304-77.696 0-140.8 63.104-140.8 140.8s63.104 140.8 140.8 140.8h89.6v51.2c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-51.2h179.2v51.2c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-51.2h89.6c77.696 0 140.8-63.104 140.8-140.8 0-46.208-22.4-87.168-56.832-112.768zM665.6 230.4c70.528 0 128 57.472 128 128 0 19.84-4.608 39.04-13.312 56.576-12.032-3.456-24.704-5.376-37.888-5.376-6.528 0-14.208 1.024-21.632 2.304a215.872 215.872 0 0 0-143.488-145.92A128.384 128.384 0 0 1 665.6 230.4z m76.8 409.6H281.6c-49.408 0-89.6-40.192-89.6-89.6s40.192-89.6 89.6-89.6c3.584 0 9.216 0.896 15.232 2.048V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-41.088C361.728 365.184 430.464 307.2 512 307.2s150.144 57.984 163.968 137.984V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-23.552c6.016-1.152 11.776-2.048 15.232-2.048 49.408 0 89.6 40.192 89.6 89.6s-40.192 89.6-89.6 89.6z m-115.2 179.2c-14.08 0-25.6 11.52-25.6 25.6v51.2c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-51.2c0-14.08-11.52-25.6-25.6-25.6z" fill="#FF8B00" p-id="16664"></path></svg>
            <svg v-if="firstPart.includes('雪')" t="1698252351582" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="17684" width="100" height="100"><path d="M857.344 681.856l-79.488-45.952 45.312-12.16c13.696-3.712 21.76-17.664 18.048-31.36a25.408 25.408 0 0 0-31.36-18.048l-94.72 25.344-70.272-40.576 83.584-22.4a25.5232 25.5232 0 0 0 3.328-48.256l-73.728-31.232 57.088-33.024 94.72 25.344c2.176 0.64 4.48 0.896 6.656 0.896a25.6 25.6 0 0 0 6.656-50.304l-45.184-12.16 79.488-45.952c12.288-7.04 16.384-22.784 9.344-34.944a25.4464 25.4464 0 0 0-34.944-9.344l-79.488 45.952 12.16-45.184a25.6 25.6 0 0 0-18.048-31.36 25.6 25.6 0 0 0-31.36 18.048l-25.344 94.592-57.088 33.024 9.856-79.488c1.28-10.24-3.712-20.224-12.544-25.344a25.6 25.6 0 0 0-28.288 1.792L537.6 358.144v-65.92l69.248-69.248c9.984-9.984 9.984-26.24 0-36.224-9.984-9.984-26.24-9.984-36.224 0L537.6 219.776V128c0-14.08-11.52-25.6-25.6-25.6s-25.6 11.52-25.6 25.6v91.776l-33.152-33.152c-9.984-9.984-26.24-9.984-36.224 0-9.984 9.984-9.984 26.24 0 36.224L486.4 292.224v65.92l-63.872-48.384c-8.704-6.656-20.736-6.912-29.696-0.768-9.088 6.144-13.312 17.28-10.496 27.904l22.4 83.712-70.272-40.576-25.344-94.72a25.5104 25.5104 0 0 0-31.36-18.048c-13.696 3.712-21.76 17.664-18.048 31.36l12.16 45.184-79.488-45.952c-12.288-7.04-27.904-2.816-34.944 9.344-7.04 12.288-2.816 27.904 9.344 34.944l79.488 45.824-45.184 12.16c-13.696 3.712-21.76 17.664-18.048 31.36 3.072 11.392 13.44 18.944 24.704 18.944 2.176 0 4.48-0.256 6.656-0.896l94.592-25.344 70.272 40.576-83.584 22.4a25.5232 25.5232 0 0 0-3.328 48.256l73.728 31.232-57.088 33.024-94.592-25.344a25.6 25.6 0 0 0-31.36 18.048 25.6 25.6 0 0 0 18.048 31.36l45.184 12.16-79.488 45.824c-12.288 7.04-16.384 22.784-9.344 34.944 4.736 8.192 13.312 12.8 22.144 12.8 4.352 0 8.704-1.152 12.8-3.456l79.488-45.952-12.16 45.312a25.6 25.6 0 0 0 24.704 32.256c11.264 0 21.632-7.552 24.704-18.944l25.344-94.72 57.088-33.024-9.856 79.488c-1.28 10.24 3.712 20.224 12.544 25.344a25.6 25.6 0 0 0 28.288-1.792L486.4 665.856v65.92l-69.376 69.376c-9.984 9.984-9.984 26.24 0 36.224 9.984 9.984 26.24 9.984 36.224 0L486.4 804.224V896c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-91.776l33.024 33.024c5.12 4.992 11.648 7.552 18.176 7.552a25.6512 25.6512 0 0 0 18.048-43.776L537.6 731.776v-65.92l63.872 48.384a25.7024 25.7024 0 0 0 29.824 0.896c9.088-6.144 13.312-17.28 10.368-27.904l-22.4-83.712 70.272 40.576 25.344 94.592c3.072 11.392 13.44 18.944 24.704 18.944 2.176 0 4.352-0.256 6.656-0.896 13.696-3.712 21.76-17.664 18.048-31.36l-12.032-45.184 79.488 45.824c4.096 2.304 8.448 3.456 12.8 3.456a25.5232 25.5232 0 0 0 12.8-47.616zM643.2 506.624l-61.056 16.384L563.2 512l39.296-22.656 40.704 17.28z m-59.136-119.424l-7.168 57.728L537.6 467.584v-45.312l46.464-35.072z m-132.992 8.448L486.4 422.4v45.312l-18.944-10.88-16.384-61.184z m-70.272 121.728l61.056-16.384 18.816 11.008-39.296 22.656-40.576-17.28z m59.136 119.424l7.168-57.728L486.4 556.288V601.6l-46.464 35.2z m132.992-8.448L537.6 601.728v-45.312l18.944 10.88 16.384 61.056z" fill="#FF8B00" p-id="17685"></path></svg>
            <svg v-if="firstPart==='中雨'" t="1698252466381" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="19603" width="100" height="100"><path d="M742.4 332.8c-6.528 0-14.208 1.024-21.632 2.304C694.016 243.328 610.048 179.2 512 179.2c-98.048 0-182.016 64.128-208.768 155.904-7.424-1.28-15.104-2.304-21.632-2.304-77.696 0-140.8 63.104-140.8 140.8s63.104 140.8 140.8 140.8c14.08 0 25.6-11.52 25.6-25.6s-11.52-25.6-25.6-25.6c-49.408 0-89.6-40.192-89.6-89.6s40.192-89.6 89.6-89.6c3.584 0 9.216 0.896 15.232 2.048V409.6c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-41.216A165.7088 165.7088 0 0 1 512 230.4c81.536 0 150.272 57.984 163.968 138.112V409.6c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-23.552c6.016-1.152 11.648-2.048 15.232-2.048 49.408 0 89.6 40.192 89.6 89.6s-40.192 89.6-89.6 89.6c-14.08 0-25.6 11.52-25.6 25.6s11.52 25.6 25.6 25.6c77.696 0 140.8-63.104 140.8-140.8s-63.104-140.8-140.8-140.8z" fill="#FF8B00" p-id="19604"></path><path d="M404.48 573.44c-9.6-12.928-31.36-12.928-40.96 0-10.24 13.568-43.52 60.544-43.52 92.16 0 37.632 26.368 64 64 64s64-26.368 64-64c0-31.616-33.28-78.592-43.52-92.16zM619.52 573.44c-10.24 13.568-43.52 60.544-43.52 92.16 0 37.632 26.368 64 64 64s64-26.368 64-64c0-31.616-33.28-78.592-43.52-92.16-9.6-12.928-31.36-12.928-40.96 0zM491.52 727.04c-10.24 13.568-43.52 60.544-43.52 92.16 0 37.632 26.368 64 64 64s64-26.368 64-64c0-31.616-33.28-78.592-43.52-92.16-9.6-12.928-31.36-12.928-40.96 0z" fill="#FF8B00" p-id="19605"></path></svg>
            <svg v-if="firstPart==='大雨'" t="1698252494482" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="19747" width="100" height="100"><path d="M742.4 409.6c-6.528 0-14.208 1.024-21.632 2.304C694.016 320.128 610.048 256 512 256c-98.048 0-182.016 64.128-208.768 155.904-7.424-1.28-15.104-2.304-21.632-2.304-77.696 0-140.8 63.104-140.8 140.8s63.104 140.8 140.8 140.8h89.6v204.8c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6V691.2h179.2v204.8c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6V691.2h89.6c77.696 0 140.8-63.104 140.8-140.8s-63.104-140.8-140.8-140.8z m0 230.4H281.6c-49.408 0-89.6-40.192-89.6-89.6s40.192-89.6 89.6-89.6c3.584 0 9.216 0.896 15.232 2.048V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-41.216A165.7088 165.7088 0 0 1 512 307.2c81.536 0 150.144 57.984 163.968 137.984V486.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6v-23.552c6.016-1.152 11.776-2.048 15.232-2.048 49.408 0 89.6 40.192 89.6 89.6s-40.192 89.6-89.6 89.6z" fill="#FF8B00" p-id="19748"></path><path d="M512 716.8c-14.08 0-25.6 11.52-25.6 25.6v230.4c0 14.08 11.52 25.6 25.6 25.6s25.6-11.52 25.6-25.6V742.4c0-14.08-11.52-25.6-25.6-25.6z" fill="#FF8B00" p-id="19749"></path></svg>
            <svg v-if="firstPart.includes('雷')" t="1698252541886" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="19891" width="100" height="100"><path d="M512 69.485714L317.44 546.377143h226.742857l-129.462857 408.137143L706.56 409.6H446.902857z" fill="#FFC931" opacity=".9" p-id="19892"></path></svg>
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
const cityName = ref('');
const isSearched = ref(false);


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
  imglistBing.value = [];
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
// 图片展示2,来自必应图片
const imglistBing = ref([])
const fetchPicBing = async () => {
  try {
    const response = await axios.get('http://localhost:5000/get_bing_img', {
      params: {
        keyword: cityChinese.value
      }
    });
    imglistBing.value = response;
  } catch (error) {
    console.log('请求百度图片信息时出错');
    console.error(error);
  }
};
function redirectToBing() {
  const url = `https://cn.bing.com/images/search?q=${cityChinese.value}&first=1`;
  window.open(url, '_blank');
}


// 获取城市天气，来自openWeatherAPI，使用后端进行整合，使用英文搜索
let firstPart = ''
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
const getWeather = async () => {
  try {
    const response = await axios.get('http://localhost:5000/get_weather', {
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
  } catch (error) {
    console.log("请求天气信息时出错")
    console.error(error);
  }
}


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
    const response = await axios.get('http://localhost:5000/get_worldbank_data', {
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


// 调用搜狗后端整理的API，获取基本信息表
const sougouBaseInfo = ref({});
const fetchSougouData = async () => {
  try {
    const response = await axios.get('http://localhost:5000/get_sougou_data', {
      params: {
        keyword: cityChinese.value
      }
    });
    sougouBaseInfo.value = response;
  } catch (error) {
    console.log("请求搜狗基本信息时出错")
    console.error(error);
  }
};


// 获取维基百科概述、百度百科综述、搜狗百科综述，使用后端进行数据获取并整合
const summary1 = ref('');
const summary2 = ref('');
const summary3 = ref('');
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
    summary3.value = response.data.summary3
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
function redirectToSougou() {
  const url = `https://baike.sogou.com/m/fullLemma?key=${cityChinese.value}`;
  window.open(url, '_blank');
}


// 调取mediastackAPI，获取新闻信息
const newslist = ref([])
const newslistWangYi = ref([])
const getnews = async() => {
  try {
    const response = await axios.get('http://api.mediastack.com/v1/news?access_key=c83a02c3414b168ce6a33859d59cb233&keywords=' + cityEnglish.value);
    newslist.value = response.data
  } catch (error) {
    console.log("请求新闻列表时出错")
    console.error(error);
  }
}
const getnewsWangYi = async() => {
  try {
    const response = await axios.get('http://localhost:5000/get_news', {
      params: {
        keyword: cityChinese.value
      }
    });
    newslistWangYi.value=response
  } catch (error) {
    console.log("请求网易新闻列表时出错")
    console.error(error);
  }
}

const validateString = (inputString) => {
  const pattern = /^[A-Z][a-z]+,\s[A-Z][a-z]+,\s[A-Z][a-z]+\s\(\p{Script=Hani}+\)$/u;
  if (!pattern.test(inputString)) {
    return false;
  }
  return true;
};

// 搜索触发请求
const getResult = async () => {
  setDefaultCityName();
  if (cityName.value === '' || cityList.value.length === 0) {
      if(!validateString(cityName.value)){
          alert('搜索结果不存在，请输入正确的城市名称');
          return
      }
  }
  isSearched.value = true;
  divide();
  fetchPic();
  fetchPicBing();
  getSummary();
  fetchSougouData();
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

.image-row {
  display: flex;
  width: 100%;
  justify-content: space-between;
}

.image-col {
  width: 30%;
  margin-bottom: 20px;
  margin-top: 20px;
}

.image-item {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.divider {
  margin: 10px 0;
  border: 0;
  border-top: 1px solid #ccc;
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
  width: 100%; 
  height: 80px;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  clip-path: polygon(0 0, 71% 0, 71% 100%, 0 100%);
  border-top-left-radius: 10px;
  border-bottom-right-radius: 10px;
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
.project-report {
  font-family: Arial, sans-serif;
  background-color: #f2f2f2;
  padding: 20px;
  border: 1px solid #ddd;
  margin: 10px;
  border-radius: 5px;
}
.info-container {
  display: flex;
  width: 100%;
}

.info-item {
  width: 100%;
  box-sizing: border-box;
  padding: 0 10px;
}

.key {
  font-weight: bold;
}

.value {
  text-align: right;
}

.info-divider {
  width: 100%;
  border: 1px solid #ccc;
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
