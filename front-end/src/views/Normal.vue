<template>
  <div>
    <recommend></recommend>
    <el-divider></el-divider>
    <el-button>一键生成报告</el-button>
    <el-button @click="toHome">HomePage</el-button>
  </div>
</template>

<script>
import Recommend from "@/components/Recommend";

export default {
  name: "Normal",
  components: {
    Recommend
  },
  methods:{
    toHome(){
      this.$router.back()
    }
  }
}
</script>

<style scoped>

</style>