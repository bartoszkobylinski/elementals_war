<template>
  <div id="app">
    <elementals-war></elementals-war>
  </div>
</template>

<script>
import ElementalsWar from "@/components/ElementalsWar.vue";

export default {
  components: {
    'elementals-war': ElementalsWar,
  },
  name: 'App',
};
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
