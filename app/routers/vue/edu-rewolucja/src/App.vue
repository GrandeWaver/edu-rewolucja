<template>
  <img alt="Vue logo" src="./assets/logo.png">
  {{ title }}
  <TestItem />
</template>

<script>
import TestItem from './components/test-item.vue'

export default {
  name: 'App',
  components: {
    TestItem
},
  data() {
    return {
      title: 'My first title'
    }
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
