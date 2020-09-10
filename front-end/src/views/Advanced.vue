<template>
  <div>
    <Analysis></Analysis>
    <el-divider></el-divider>
    <Recommend :chartData="chartData"></Recommend>
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
        data() {
            return {
                chartData: [
                    ['x-line', 'number1', 'number2'],
                    [20, 25, 30],
                    [25, 40, 56],
                    [30, 56, 24]
                ]
            }
        },
        components: {
            Analysis,
            Recommend
        },
        methods: {
            toHome() {
                this.$router.back()
            }
        }
    }
</script>

<style scoped>

</style>