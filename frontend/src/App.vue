<template>
  <MainpageComponent/>
</template>

<script>
import MainpageComponent from './components/MainPage.vue'

export default {
  name: 'App',
  components: {
    MainpageComponent
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
