<template>
  <div class="about">
    <h1>This is an about page</h1>
    <el-button id="getData" @click="getData">getFvData测试</el-button>
    <div>{{outputData}}</div>
  </div>
</template>


<script>
import {getFvDataAPI} from "@/api/output";
export default {
  data(){
    return {
      outputData:''
    }
  },
  methods:{
    // 测试用
    async getData(){
      let that=this
      const res =await getFvDataAPI()
      console.log(res)
      that.outputData=res
    }

  }
}
</script>