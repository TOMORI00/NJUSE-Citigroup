<template>
  <div>
    <div class="div-heading">
      <div class="div-logo">
        <a @click="toHomepage">
          <img class="logo-img" src="../assets/nju.png">
        </a>
      </div>
      <div class="div-name">
        <h2 style="margin:auto;font-size: 25px">公募基金/理财复现与顾问组合系统（EPC）</h2>
        <el-dropdown style="float: right;margin-top: 10px;margin-right: 20px">
          <el-avatar icon="el-icon-user-solid"></el-avatar>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item disabled>{{this.userName}}</el-dropdown-item>
            <el-dropdown-item divided @click="signOut"><a @click="signOut">退出登录</a></el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
        <!--        <h3>{{this.userName}}</h3>-->
      </div>
    </div>
    <el-divider id="heading-divider" style="margin: 0;padding: 0;height: 2px"></el-divider>
  </div>
</template>

<script>
    import Global from "./GlobalData";

    export default {
        name: "Heading",
        data() {
            return {
                userName: Global.userName
            }
        },
        methods: {
            toHomepage() {
                this.$router.push('/homepage')
            },
            signOut(){
                console.log("sign out")
                Global.isAuthenticated = false
                this.$router.push('/login')
            },
        },
    }
</script>

<style scoped>
  .div-heading {
    width: 100%;
    height: 120px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    /*background: url("https://mjh1.oss-cn-hangzhou.aliyuncs.com/1542.jpg");*/
    /*background-position: center center;*/
    /*background-repeat: no-repeat;*/
    /*background-size:2059.86px 130px;*/
    /*background: -moz-linear-gradient(top, #000000 0%, #ffffff 100%);*/
    /*background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#000000), color-stop(100%,#ffffff));*/
    /*background: -webkit-linear-gradient(top, #000000 0%,#ffffff 100%);*/
    /*background: -o-linear-gradient(top, #000000 0%,#ffffff 100%);*/
    /*background: -ms-linear-gradient(top, #000000 0%,#ffffff 100%);*/
    /*background: linear-gradient(to bottom, #000000 0%,#ffffff 100%);*/
  }

  @media screen and (max-width: 1440px) {
    .div-heading {
      width: 1440px;
    }
  }

  .div-logo {
    width: 60px;
    position: relative;
    top: 10px;
    left: 40px;
    float: left;
    margin: 0;
    padding: 0;
  }

  .logo-img {
    width: 70.02px;
    height: 85.15px;
  }

  .div-name {
    float: right;
    height: 100px;
    position: relative;
    margin: 0;
    padding-top: 12px;
    right: 40px;
  }

  #heading-divider {
    margin: 0;
    padding: 0;
    height: 1px;
  }
</style>