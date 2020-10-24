此页为首页
- 本页元素与交互
- 图片背景
- 左上图标》跳转至某页面（目前为NJU主页）
- 上方中央软件名称
- 右上“关于”按钮》跳转至“关于”页面
- 中央选择框
- 选择提示语句
- Advanced：高级用户》银行经理
- Normal：普通用户》个人客户
- Analysis：分析用户》数据分析者

<template>
  <div class="div-background-image">
    <div class="div-homepage">
      <el-container height="617px">
        <el-header class="homepage-header" height="100px">
          <div class="div-logo">
            <a href="https://www.nju.edu.cn/">
              <img class="logo-img" src="../assets/nju.png">
            </a>
          </div>
          <div class="div-more-link">
            <div class="link-text">
              <a href="/about"><h2>关于</h2></a>
            </div>
          </div>
        </el-header>

        <div class="title" >公募基金分析推荐系统</div>

        <el-divider></el-divider>
        <el-main>
          <div class="div-choose" id="div-choose">
            <h1 style="position: relative;top:40px; font-size:30px;">请选择您的用户类型</h1>
            <el-button class="choose-button" @click="toAdvanced">专业用户</el-button>
            <el-button class="choose-button" @click="toNormal">普通用户</el-button>
            <el-button class="choose-button" @click="toAnalysis">分析用户</el-button>
          </div>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      reportURL: "https://mjh1.oss-cn-hangzhou.aliyuncs.com/illust_80820235_20200817_194855.jpg"
    }
  },
  methods: {
    toAdvanced() {
      this.$router.push('/advanced')
    },
    toNormal() {
      this.$router.push('/normal')
    },
    toAnalysis() {
      //TODO，下载pdf
      window.open(this.reportURL)
    }
  }
}

</script>

<style scoped>
.div-background-image {
  width: 100%;
  position: fixed;
  background-image: url("https://mjh1.oss-cn-hangzhou.aliyuncs.com/1542.jpg");
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  height: 100%;
}

.div-homepage {
  position: center;
  margin: auto;
  width: 1440px;
  height: 617px;
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
  width: 131.58px;
  height: 164.74px;
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
  display: inline-block;
  border-radius: 10px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 80px;
  height: 30px;
  background: rgba(255, 254, 254, 0.4);
  margin-top: 25px;
  margin-left: auto;
  margin-right: auto;
}
.div-choose {
  border-radius: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 1000px;
  height: 400px;
  background: rgba(0, 0, 0, 0.25);
  margin-top: 25px;
  margin-left: auto;
  margin-right: auto;
}

.div-more-link {
  width: 150px;
  height: 30px;
  margin: auto;
  position: relative;
  top: 30px;
  right: -450px;
  display: inline-block;
}

.choose-button {
  margin: 50px;
  width: 200px;
  height: 200px;
  position: relative;
  top: 15px;
  opacity: 0.9;
  font-weight:bold; 
  font-size:26px;
  background-image: url('../assets/user.png');
  padding: 14% 0% 0%;
}

.choose-button--active

.title {
  border-radius: 12px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.3);
  width: 500px;
  height: 60px;
  background: rgba(0, 0, 0, 0.1);
  margin-top: 25px;
  margin-left: auto;
  margin-right: auto;
  font-weight:bold;
  font-size:40px;
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
</style>