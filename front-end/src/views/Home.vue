此页为入口页
- 本页元素与交互
  - 图片背景
  - 左上图标》跳转至某页面（目前为NJU主页）
  - 上方中央软件名称
  - 右上“关于”按钮》跳转至“关于”页面
  - 中央登录框
    - 输入用户名
    - 输入密码
    - 点击登录

<template>
  <div class="div-background-image">
    <div class="div-homepage">
      <el-container height="817px">
        <el-header class="homepage-header" height="160px">
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
                
        <div class="title">公募基金分析推荐系统</div>

        <el-divider></el-divider>
        <el-main>
          <el-form :model="ruleForm" :rules="rules" ref="ruleForm" class="div-choose">
            <el-form-item prop="name">
              <el-input v-model="ruleForm.name" placeholder="用户名"></el-input>
            </el-form-item>
            <el-form-item prop="password">
              <el-input v-model="ruleForm.password" placeholder="密码" show-password></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type='primary' @click="login('ruleForm')" class="choose-button">登录</el-button>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
    </div>
  </div>
</template>

<script>

export default {
  name: 'Home',
  data() {
    return {
      ruleForm:{
        name:'',
        password:''
      },
      rules: {
        name: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods:{
    login(formName){
      this.$refs[formName].validate((valid) => {
          if (valid) {
            this.$router.push('/homepage')
          } else {
            console.log('error submit!!');
            return false;
          }
        });
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
  width: 131.58px;
  height: 164.74px;
  position: relative;
  top: 15px;
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

.link-text {
  display: inline-block;
  border-radius: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 80px;
  height: 30px;
  background: rgba(255, 254, 254, 0.4);
  margin-top: 25px;
  margin-left: auto;
  margin-right: auto;
}

.div-choose {
  width: 800px;
  height: 450px;
  margin-top: 25px;
  margin-left: auto;
  margin-right: auto;
}

.title {
  border-radius: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  width: 500px;
  height: 60px;
  background: rgba(255, 254, 254, 0.4);
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
