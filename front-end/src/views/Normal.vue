<template>
  <div>
    <recommend></recommend>
    <el-divider></el-divider>
    <el-button>一键生成报告</el-button>
    <el-button @click="toHome">HomePage</el-button>
    <GChart 
      type="LineChart"
      :data="chartData"
      :options="chartOption"/>
  </div>
</template>

<script>
import Recommend from "@/components/Recommend";
import {GChart} from 'vue-google-charts';

export default {
  name: "Normal",
  data(){
    return {
      chartData:[
        ['x-line','number1','number2'],
        [20,25,30],
        [25,40,56],
        [30,56,24]
      ],
      //chartOption控制表格属性，更多选项请参考官方API：“https://developers.google.cn/chart/interactive/docs/gallery/linechart?hl=en#configuration-options”
      chartOption:{
        charts:{
          title:'testChart'
        },
        focusTarget:'category'
      }
    }
  },
  components: {
    Recommend,
    GChart
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