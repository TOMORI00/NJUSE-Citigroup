<template>
  <div>
    <heading></heading>
    <div class="div-normal">
      <el-container>
        <el-header class="normal-head"></el-header>
        <el-divider id="divider-1"></el-divider>
        <el-main>
          <recommend :chartData="chartData"></recommend>
          <el-divider></el-divider>
          <el-button>一键生成报告</el-button>
          <el-button @click="toHome">HomePage</el-button>
        </el-main>
      </el-container>
    </div>
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

  }

  #divider-1 {
    margin: 0;
  }


</style>