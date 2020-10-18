<template>
  <div class="div-main">
    <!--    1-->
    <heading></heading>

    <!--    3-->
    <el-container id="my-container">
      <el-header height="40px" style="margin: 20px">
        <el-radio-group v-model="radio" @change="changePieChart(radio)">
          <el-radio :label="3">低风险</el-radio>
          <el-radio :label="6">中风险</el-radio>
          <el-radio :label="9">高风险</el-radio>
        </el-radio-group>
      </el-header>

      <el-divider></el-divider>

      <!--      5-->
      <div class="div-result" id="div-result">
        <GChart class="analysis-chart" type="PieChart" :data=chartData :options="chartOption"/>
      </div>
    </el-container>
  </div>
</template>

<script>
    import Heading from "../components/Heading";
    import XLSX from 'xlsx'
    import {importExcelAPI} from "@/api/upload";

    export default {
        name: "Advanced",
        data() {
            return {
                radio: 3,
                // 画图
                chartData: [
                    ['name', 'contribution'],
                    ['ss', 25],
                    ['ljl', 40],
                    ['dqj', 56],
                    ['mjh',100]
                ],
                // 画图
                chartOption: {
                    charts: {
                        title: 'testChart'
                    },
                    is3D:true
                },
            }
        },
        components: {
            Heading
        },
        methods: {
            changePieChart(val){
                if(val==3)this.chartData=[
                    ['name', 'contribution'],
                    ['ss', 25],
                    ['ljl', 40],
                    ['dqj', 56],
                    ['mjh',100]
                ]
                else if(val==6)this.chartData=[
                    ['name', 'contribution'],
                    ['ss', 75],
                    ['ljl', 40],
                    ['dqj', 56],
                    ['mjh',100]
                ]
                else this.chartData=[
                    ['name', 'contribution'],
                    ['ss', 125],
                    ['ljl', 40],
                    ['dqj', 56],
                    ['mjh',100]
                ]
            }
        }
    }
</script>

<style scoped>
  .div-main {
    width: 100%;
  }

  @media screen and (max-width: 1440px) {
    .div-main {
      width: 1440px;
    }
  }

  .analysis-chart {
    width: 960px;
    height: 480px;
    margin: auto;
  }
</style>