<template>
  <div>
    <div class="my-div">
      <el-carousel
          class="my-carousel"
          arrow="never"
          height="450px">
        <el-carousel-item
            class="my-carousel-item"
            v-for="item in URLs"
            v-bind:key="item.name">
          <div>
            <img class="my-carousel-image" v-bind:src="item.url">
          </div>
        </el-carousel-item>
      </el-carousel>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  data() {
    return {
      URLs: [
        {
          name: "pic1",
          url: "https://mjh1.oss-cn-hangzhou.aliyuncs.com/illust_68295293_20191216_202417.jpg"
        },
        {
          name: "pic2",
          url: "https://mjh1.oss-cn-hangzhou.aliyuncs.com/illust_77353796_20200102_102318.jpg"
        },
        {
          name: "pic3",
          url: "https://mjh1.oss-cn-hangzhou.aliyuncs.com/illust_80119487_20200725_124007.jpg"
        }
      ]
    }
  }
}
</script>

<style scoped>

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}

.my-div {
  width: 800px;
  height: 450px;
  margin: auto
}

.my-carousel {
  width: 800px;
  margin: auto;
}

.my-carousel-item {
  width: 800px;
  height: 450px;
}

.my-carousel-image {
  width: 800px;
  height: 450px;
}
</style>