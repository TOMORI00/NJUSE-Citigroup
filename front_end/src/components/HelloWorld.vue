<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <a-input type="text" v-model="username"></a-input>
    <a-button type="primary" @click="helloPost">提交</a-button>
  </div>
</template>

<script>
import {
  getAPI,
  postAPI
  } from '@/api/hello'

export default {
  name: 'HelloWorld',

  props: {
    msg: String
  },
  data(){
    return{
          username:''
    }
  },

  methods:{
    helloGet(){
      const res=getAPI()
      console.log(res)
    },
    helloPost(){
      console.log("helloPost")
      const data={
        i:this.username
      }
      const res=postAPI(data);
      if(res){
        console.log("HelloPost ok",res)
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
