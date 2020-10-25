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
  <div>
    <div class="div-bg"></div>
    <div class="div-main">

      <heading></heading>

      <el-container>
        <el-aside></el-aside>
        <el-main>
          <div class="mainblock">

            <el-header height="40px" style="margin: 20px">
              <div class="div-risk">
                <el-radio-group v-model="radio" @change="changePieChart(radio)">
                  <el-radio :label="3">瑞安组合</el-radio>
                  <el-radio :label="6">瑞衡组合</el-radio>
                  <el-radio :label="9">瑞利组合</el-radio>
                </el-radio-group>
              </div>
            </el-header>

            <el-container>
              <el-main>
                <el-tabs v-model="activeName">

                  <el-tab-pane label="实时推荐" name="first">

                    <p style="font-weight:bold;
                          font-size:20px;
                          border-radius: 15px;
                          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                          background: rgba(0, 0, 0, 0.15);
                          margin-top: 25px;
                          padding:1%;"
                    >投资建议</p>
                    <div style="width: 800px;height: 480px;margin: auto">
                      <GChart type="PieChart" :data=recommendPie :options="PieChartOptions"/>
                    </div>
                    <el-divider></el-divider>

                  </el-tab-pane>

                  <el-tab-pane label="推荐历史" name="third">
                    <p style="font-weight:bold;
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.15);
                        margin-top: 25px;
                        padding:1%;"
                    >历史推荐</p>
                    <div class="timeblock">
                      <span style="font-weight:bold; font-size:15px;">开始时间:   </span>
                      <el-date-picker v-model="dateValue" type="month" format="yyyy年MM月" placeholder="请选择时段"
                                      @change="handleDateChange">
                      </el-date-picker>
                      <br>
                      <el-button @click="getRecommendCombination" style="margin-top: 20px">查看历史推荐组合</el-button>
                    </div>
                    <div style="width: 800px;height: 480px;margin: auto">
                      <GChart type="PieChart" :data=historyPie :options="PieChartOptions" v-if="historyPieDisplay"/>
                    </div>
                  </el-tab-pane>

                </el-tabs>
              </el-main>
            </el-container>
          </div>
        </el-main>
        <el-aside></el-aside>
      </el-container>


    </div>
  </div>
</template>

<script>
import Heading from "../components/Heading";
import XLSX from 'xlsx'
import {importExcelAPI} from "@/api/upload";
import {getChartAPI} from "@/api/output";

export default {
  name: "Advanced",
  data() {
    return {
      dateValue:'',
      month:'',
      year:'',
      radio: 3,
      // 画图
      chartData: '',
      // 画图
      PieChartOptions: {
        charts: {
          title: 'testChart'
        },
        is3D: true,
        width: 800,
        height: 480,
      },
      pieData:'',
      risked_history:'',
      recommendPie:'',
      historyPie:'',
      historyPieDisplay:false,

      //默认实时推荐页面
      activeName: 'first',
    }
  },
  created(){
    let that=this
    this.getChartData()
    console.log('created')
  },
  components: {
    Heading
  },
  methods: {
    recommendChange(val){
      let that=this
      that.dateValue= ''
      that.month=''
      that.year=''
      that.historyPieDisplay=false
      that.historyPie=[['name', 'contribution']]
      if (val === 3) {
        that.risked_history=that.chartData.history_low
        that.recommendPie=that.risked_history[that.risked_history.length-1]['pieData']
      } else if (val === 6) {
        that.risked_history=that.chartData.history_mid
        that.recommendPie=that.risked_history[that.risked_history.length-1]['pieData']
      } else if (val === 9) {
        that.risked_history=that.chartData.history_high
        that.recommendPie=that.risked_history[that.risked_history.length-1]['pieData']
      }

    },
    // click to get recommend combination
    getRecommendCombination() {
      for (let index = 0; index < this.risked_history.length; index++) {
        const element = this.risked_history[this.risked_history.length-1-index];
        if(this.year>=element['year'] && this.month>=element['month']){
          this.historyPie=element['pieData']
          break
        }
      }
      this.historyPieDisplay=true
      console.log('getRecommendCombination')
    },

    // date Change
    handleDateChange(value) {
      var selectedDate=new Date(value)
      this.month=selectedDate.getMonth()+1
      this.year=selectedDate.getFullYear()
      console.log(value)
    },
    async getChartData(){
      let that=this
      console.log('getChartData')
      this.chartData=await getChartAPI()
      console.log(that.chartData)
      that.risked_history=that.chartData.history_low
      that.recommendPie=that.risked_history[that.risked_history.length-1]['pieData']
      console.log(that.recommendPie)
    }
  },

}
</script>

<style scoped>
.div-bg {
  z-index: -1;
  width: 100%;
  position: fixed;
  background-image: url("https://mjh1.oss-cn-hangzhou.aliyuncs.com/1542.jpg");
  /* background-image: url("../assets/background.jpg"); */
  background-position: center center;
  background-repeat: no-repeat;
  background-size: cover;
  height: 100%;
}

.div-main {
  width: 100%;
  /*background-image: url("https://mjh1.oss-cn-hangzhou.aliyuncs.com/1542.jpg");*/
  /*background-position: center center;*/
  /*background-repeat: no-repeat;*/
  /*background-size: 100%;*/
  /*background-attachment: fixed;*/
}

@media screen and (max-width: 1440px) {
  .div-main {
    width: 1440px;
    /*background-size: 1440px;*/
  }
}

.mainblock {
  border-radius: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
  background: rgba(0, 0, 0, 0.15);
  /*margin-top: 25px;*/
  padding: 5%;
}

.div-risk {
  border-radius: 15px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background: rgba(0, 0, 0, 0.09);
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
</style>