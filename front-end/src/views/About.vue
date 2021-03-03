<template>
  <div class="about">
    <h1>This is an about page</h1>
    本系统由NJU花旗杯团队-“精神小伙”提供
  </div>
</template>


<script>
import {getFvDataAPI} from "@/api/output";
import {getChartAPI} from "@/api/output";
export default {
  data(){
    return {
      outputData:'',
      chartData:'',
      pieData:'pie'
    }
  },
  methods:{
    // 测试用
    async getData(){
      let that=this
      const res =await getChartAPI()
      console.log(res)
      that.chartData=res
      let risked_history=that.chartData.history_low
      that.pieData=risked_history[risked_history.length-1]['pieData']
    }

  }
}
</script>