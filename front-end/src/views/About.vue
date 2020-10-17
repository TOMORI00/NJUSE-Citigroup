<template>
  <div class="about">
    <h1>This is an about page</h1>
    <el-button id="getData" @click="getData">getData</el-button>
    <div>{{outputData}}</div>
  </div>
</template>


<script>
import {getDataAPI} from "@/api/output";
export default {
  data(){
    return {
      outputData:''
    }
  },
  methods:{
    async getData(){
      let that=this
      const res =await getDataAPI()
      console.log(res)
      that.outputData=res
    }

  }
}
</script>