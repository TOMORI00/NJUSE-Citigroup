<template>
  <div class="demo-image__placeholder">
    <br>
    <div class="block">
      <el-image :src="src"></el-image>
    </div>
    <div>
      <div>
        <el-button-group>
          <el-button type="primary" icon="el-icon-picture" v-bind:title="buttonMessages[0]"
                     @click="getPicture"></el-button>
          <el-button type="primary" icon="el-icon-download" v-bind:title="buttonMessages[1]"
                     @click="getReport"></el-button>
          <el-button type="primary" icon="el-icon-more" v-bind:title="buttonMessages[2]" @click="getMore"></el-button>
        </el-button-group>
      </div>
      <el-divider></el-divider>
      <div>
        <a href="https://mjh1.oss-cn-hangzhou.aliyuncs.com/illust_80820235_20200817_194855.jpg"
           download="test">
          <el-button round>保存配信息至本地</el-button>
        </a>
      </div>
    </div>
    <el-divider></el-divider>
  </div>
</template>

<script>
export default {
  data() {
    return {
      current: {
        name: "",
        content: {}
      },
      src:"https://mjh1.oss-cn-hangzhou.aliyuncs.com/illust_80820235_20200817_194855.jpg",
      buttonMessages: [
        "下载图片",
        "生成报告",
        "更多",
      ]
    }
  },
  methods: {
    getPicture() {
      window.open(this.src)
      console.log("download-download")
    },
    getReport() {
      console.log('download-report')
    },
    getMore() {
      console.log("download-more")
    },
    saveInfo() {
      console.log("save info")
    }
  }
}
</script>

<style></style>