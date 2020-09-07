<template>
  <div class="my-homepage">
    <el-header class="my-header" height="200px">
      <div class="div-logo">
        <a href="https://www.nju.edu.cn/">
          <img class="logo-img" src="../assets/logo.png">
        </a>
      </div>
      <div class="div-about">
        <router-link class="home-link" to="/home">
          <h2>Home</h2>
        </router-link>
        <router-link class="about-link" to="/about">
          <h2>About</h2>
        </router-link>
      </div>
    </el-header>
    <el-main>
      <div>
        <el-button @click="toAdvanced">Advanced</el-button>
        <el-button @click="toNormal">Normal</el-button>
      </div>
      <el-divider></el-divider>
    </el-main>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  methods: {
    toAdvanced() {
      this.$router.replace('/advanced')
    },
    toNormal() {
      this.$router.replace('/normal')
    }
  }
}

</script>

<style scoped>
.my-homepage {
  margin: auto;
  width: 100%;
  height: 900px;
  background-image: url("https://mjh1.oss-cn-hangzhou.aliyuncs.com/illust_83645290_20200817_194209.jpg");
  background-position: center top;
  background-repeat: no-repeat;
  background-size: 1600px 900px;
}

.div-logo{
  width: 300px;
  height: 200px;
  float: left;
}

.logo-img {
  width: 130px;
  height: 130px;
  position: absolute;
  top: 35px;
  left:80px
}

.div-about{
  height: 200px;
  float: left;
}

.about-link{
  position: absolute;
  top: 90px;
  right: 90px;
}

.home-link{
  position: absolute;
  top: 90px;
  right: 160px;
}
</style>