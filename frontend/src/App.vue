<template>
  <div id="app">

    <div class="text-center">
      <img alt="Vue logo" width="100" src="./assets/logo.png">
    </div>

    <div class="px-5 my-5">
      <WeatherForecast/>
    </div>

  </div>
</template>

<script>
import WeatherForecast from './components/WeatherForecast.vue'

export default {
  name: 'App',
  components: {
    WeatherForecast,
  }
}
</script>

<style>
#app {
  margin-top: 20px;
}
</style>
