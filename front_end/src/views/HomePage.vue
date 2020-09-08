<template>
  <div class="my-homepage">
    <el-container height="818px">
      <el-header height="160px">
        <div class="div-logo">
          <a href="https://www.nju.edu.cn/">
            <img class="logo-img" src="../assets/logo.png">
          </a>
        </div>
        <div class="div-more">
          <div class="more-link">
            <a href="/home"><h2>Home</h2></a>
          </div>
          <div class="more-link">
            <a href="/about"><h2>About</h2></a>
          </div>
        </div>
      </el-header>
      <el-divider></el-divider>
      <el-main>
        <div class="div-choose">
          <h1 style="position: relative;top:58px;font-family: 楷体">首次进入请选择一个身份</h1>
          <el-button class="choose-button" @click="toAdvanced">Advanced</el-button>
          <el-button class="choose-button" @click="toNormal">Normal</el-button>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  methods: {
    toAdvanced() {
      this.$router.push('/advanced')
    },
    toNormal() {
      this.$router.push('/normal')
    }
  }
}

</script>

<style scoped>
.my-homepage {
  margin: auto;
  width: 1440px;
  height: 817px;
  /*background-image: url("https://mjh1.oss-cn-hangzhou.aliyuncs.com/illust_83645290_20200817_194209.jpg");*/
  /*background-position: center top;*/
  /*background-repeat: no-repeat;*/
  /*background-size: 1600px 900px;*/
}

.div-logo {
  width: 300px;
  height: 200px;
  display: inline-block;
}

.logo-img {
  width: 130px;
  height: 130px;
  position: relative;
  top: 25px;
  left: -100px;
}

.div-more {
  width: 800px;
  height: 200px;
  display: inline-block;
}

.more-link {
  width: 70px;
  height: 30px;
  display: inline-block;
  margin: auto;
  position: relative;
  top: 25px;
  right: -350px;
}

.div-choose {
  border-radius: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 800px;
  height: 450px;
  background: white;
  margin-top: 25px;
  margin-left: auto;
  margin-right: auto;
}

.choose-button {
  margin: 50px;
  width: 200px;
  height: 200px;
  position: relative;
  top: 65px;
}
</style>