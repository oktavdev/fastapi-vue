<template>
  <div id="app">

    <div class="text-center">
    <img alt="Vue logo" width="100" src="./assets/logo.png">

    <HelloWorld msg="Vue.js App"/>
    </div>


    <div class="px-5 py-5 my-5">
      <WeatherForecast/>
    </div>


  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import WeatherForecast from './components/WeatherForecast.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    WeatherForecast,
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
