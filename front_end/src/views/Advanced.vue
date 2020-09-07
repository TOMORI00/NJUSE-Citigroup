<template>
  <div>
    <Analysis></Analysis>
    <el-divider></el-divider>
    <Recommend></Recommend>
    <el-divider></el-divider>
    <el-button>一键生成报告</el-button>
    <el-button @click="toHome">HomePage</el-button>
  </div>
</template>

<script>
import Analysis from "@/components/Analysis";
import Recommend from "@/components/Recommend";

export default {
  name: "Advanced",
  components: {
    Analysis,
    Recommend
  },
  methods:{
    toHome(){
      this.$router.replace('/')
    }
  }
}
</script>

<style scoped>

</style>