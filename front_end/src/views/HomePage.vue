<template>
  <div>
    <el-divider>HomePage</el-divider>
    <div>
      <el-button @click="toAdvanced">Advanced</el-button>
      <el-button @click="toNormal">Normal</el-button>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  methods: {
    toAdvanced() {
      this.$router.replace('/advanced')
    },
    toNormal() {
      this.$router.replace('/normal')
    }
  }
}

</script>

<style scoped>

</style>