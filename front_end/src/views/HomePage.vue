<template>
  <div class="div-background-image">
    <div class="div-homepage">
      <el-container height="817px">
        <el-header class="homepage-header" height="160px">
          <div class="div-logo">
            <a href="https://www.nju.edu.cn/">
              <img class="logo-img" src="../assets/logo.png">
            </a>
          </div>
          <div class="div-more-link">
            <div class="link-text">
              <a href="/home"><h2>Home</h2></a>
            </div>
            <div class="link-text">
              <a href="/about"><h2>About</h2></a>
            </div>
          </div>
        </el-header>
        <el-divider></el-divider>
        <el-main>
          <div class="div-choose" id="div-choose">
            <h1 style="position: relative;top:58px;font-family: 楷体">首次进入请选择一个身份</h1>
            <el-button class="choose-button" @click="toAdvanced">Advanced</el-button>
            <el-button class="choose-button" @click="toNormal">Normal</el-button>
          </div>
        </el-main>
      </el-container>
    </div>
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
.div-background-image {
  width: 100%;
  position: fixed;
  background-image: url("https://mjh1.oss-cn-hangzhou.aliyuncs.com/illust_83645290_20200817_194209.jpg");
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  height: 100%;
}

.div-homepage {
  position: center;
  margin: auto;
  width: 1440px;
  height: 817px;
}

.div-logo {
  width: 160px;
  height: 160px;
  display: inline-block;
  position: relative;
  top: 10px;
  left: -475px;
}

.logo-img {
  margin: auto;
  width: 130px;
  height: 130px;
  position: relative;
  top: 15px;
}

/*.div-more {*/
/*  width: 800px;*/
/*  height: 160px;*/
/*  display: inline-block;*/
/*  position: relative;*/
/*  !*right: 20px;*!*/
/*  top: -46px;*/
/*}*/

.div-more-link {
  width: 150px;
  height: 30px;
  margin: auto;
  position: relative;
  top: 30px;
  right: -450px;
  display: inline-block;
}

.link-text {
  width: 70px;
  height: 30px;
  display: inline-block;
  margin: auto;
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

@media screen and (max-width: 1170px) {
  .div-choose {
    position: absolute;
    right: 50px;
  }
}

@media screen and (max-width: 900px) {
  .div-choose {
    position: absolute;
    left: 50px;
  }
}

.choose-button {
  margin: 50px;
  width: 200px;
  height: 200px;
  position: relative;
  top: 65px;
}
</style>