此页为个人用户页，是个人使用的页面
- 本页元素与交互
  - 图片背景
  - 左上图标》跳转至某页面（目前为NJU主页）
  - 右上软件名称
  - 中央
    - 理财、基金选择框
    - excel上传
    - 功能页
      - 推荐
        - 实时推荐
        - 推荐历史

<template>
  <div class="div-main">

    <heading></heading>

    <el-container>
      <el-aside></el-aside>
      <el-main>
        <div class="mainblock">

          <el-header height="40px" style="margin: 20px">
            <div class="div-risk">
              <el-radio-group v-model="radio" @change="changePieChart(radio)">
                <el-radio :label="3">低风险</el-radio>
                <el-radio :label="6">中风险</el-radio>
                <el-radio :label="9">高风险</el-radio>
              </el-radio-group>
            </div>
          </el-header>

          <el-container>
            <el-main>
              <el-tabs v-model="activeName" >
                    
                    <el-tab-pane label="实时推荐" name="first">

                        <p style="font-weight:bold; 
                          font-size:20px;
                          border-radius: 15px;
                          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                          background: rgba(0, 0, 0, 0.15);
                          margin-top: 25px;
                          padding:1%;"
                          >投资建议</p>
                        <GChart type="PieChart" :data=chartData :options="PieChartOptions"/>
                        <el-divider></el-divider>

                    </el-tab-pane>

                    <el-tab-pane label="历史推荐" name="third">
                      <p style="font-weight:bold; 
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.15);
                        margin-top: 25px;
                        padding:1%;"
                        >历史推荐记录</p>
                      <div class="timeblock">
                        <span style="font-weight:bold; font-size:15px;">选择时段:   </span>
                        <el-date-picker v-model="dateValue" type="month" format="yyyy年MM月" placeholder="请选择时段"
                                        @change="handleDateChange">
                        </el-date-picker>
                        <br>
                        <el-button @click="getRecommendCombination" style="margin-top: 20px">查看历史推荐组合</el-button>
                      </div>
                      <GChart type="PieChart" :data=chartData :options="PieChartOptions"/>
                    </el-tab-pane>
                    
              </el-tabs>
            </el-main>
          </el-container>
        </div>
      </el-main>
      <el-aside></el-aside>
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
                PieChartOptions: {
                    charts: {
                        title: 'testChart'
                    },
                    is3D:true,
                    width:960,
                    height:480,
                },

                //默认实时推荐页面
                activeName: 'first',
            }
        },
        components: {
            Heading
        },
        methods: {
            changePieChart(val){
                if(val===3)this.chartData=[
                    ['name', 'contribution'],
                    ['ss', 25],
                    ['ljl', 40],
                    ['dqj', 56],
                    ['mjh',100]
                ]
                else if(val===6)this.chartData=[
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

  .mainblock {
  border-radius: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.075);
  margin-top: 25px;
  padding:5%;
}

.div-risk {
  border-radius: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.107);
  margin-top: 25px;
  margin-bottom: 25px;
  padding: 2%;
}

.timeblock {
  border-radius: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.092);
  margin-top: 25px;
  margin-bottom: 25px;
  padding: 2%;
}

  @media screen and (max-width: 1440px) {
    .div-main {
      width: 1440px;
    }
  }
</style>