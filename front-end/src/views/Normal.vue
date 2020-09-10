<template>
  <div class="div-normal">
    <el-container>
      <el-header class="normal-head" height="60px">
        <div class="div-logo">
          <a href="/">
            <img class="logo-img" src="../assets/logo.png">
          </a>
        </div>
        <div class="div-name"><h2 style="margin:auto;font-size: 24px">花旗杯</h2></div>
      </el-header>
      <el-divider id="divider-1"></el-divider>
      <el-main>
        <recommend :chartData="chartData"></recommend>
        <el-divider></el-divider>
        <el-button>一键生成报告</el-button>
        <el-button @click="toHome">HomePage</el-button>
      </el-main>
    </el-container>
  </div>
</template>

<script>
    import Heading from "../components/Heading";
    import Recommend from "@/components/Recommend";

    export default {
        name: "Normal",
        data() {
            return {
                chartData: [
                    ['x-line', 'number1', 'number2'],
                    [20, 25, 30],
                    [25, 40, 56],
                    [30, 56, 24]
                ]
            }
        },
        components: {
            Recommend,
            // eslint-disable-next-line vue/no-unused-components
            Heading
        },
        methods: {
            toHome() {
                this.$router.back()
            }
        }
    }
</script>

<style scoped>
  .div-normal {
    width: 1440px;
    margin: auto;
  }

  .normal-head {
    margin: 0;
    padding: 0;
  }

  .div-logo {
    width: 50px;
    position: relative;
    top: 5px;
    left: 40px;
    float: left;
    margin:0;
    padding: 0;
  }

  .logo-img {
    width: 50px;
    height: 50px;
  }

  .div-name {
    float: right;
    height: 60px;
    position: relative;
    margin: 0;
    padding-top: 12px;
    right: 40px;
  }

  #divider-1 {
    margin: 0;
  }


</style>