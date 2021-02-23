2021-2-23 mjh
背景图片组件

<template>
  <div class="bgp">
  </div>
</template>

<script>
    export default {
        name: "BackGround"
    }
</script>

<style scoped>
  .bgp {
    z-index: -1;
    width: 100%;
    position: fixed;
    background-image: url("../assets/1542.jpg");
    /* background-image: url("../assets/background.jpg"); */
    background-position: center center;
    background-repeat: no-repeat;
    background-size: cover;
    height: 100%;
  }
</style>