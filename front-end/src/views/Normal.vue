此页为个人用户页，是个人使用的页面
- 本页元素与交互
- 图片背景
- 左上图标》跳转至某页面（目前为主页）
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

            <el-header height="140px" style="margin: 20px">
              <div class="div-risk">
                <el-radio-group v-model="radio" @change="recommendChange">
                  <el-radio :label="3">低风险</el-radio>
                  <el-radio :label="6">中风险</el-radio>
                  <el-radio :label="9">高风险</el-radio>
                </el-radio-group>
              </div>
              <p v-if='radio==3' style="font-weight:bold;
                          font-size:20px;
                          border-radius: 15px;
                          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                          background: rgba(0, 0, 0, 0.15);
                          margin-top: 25px;
                          padding:1%;"
                    >低风险组合：防御为主，稳中有进。<br>历史模拟中，可能承受的最大亏损约5%  <br>目标为获取超越理财产品的收益</p>
              <p v-if='radio==6' style="font-weight:bold;
                          font-size:20px;
                          border-radius: 15px;
                          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                          background: rgba(0, 0, 0, 0.15);
                          margin-top: 25px;
                          padding:1%;"
                    >中风险组合：进攻为主，攻守兼备。<br>历史模拟中，可能承受的最大亏损约15%  <br>目标为获取远高于理财产品和信托产品的收益</p>
              <p v-if='radio==9' style="font-weight:bold;
                          font-size:20px;
                          border-radius: 15px;
                          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                          background: rgba(0, 0, 0, 0.15);
                          margin-top: 25px;
                          padding:1%;"
                    >高风险组合：主动进攻，追求高收益。<br>历史模拟中,可能承受的最大亏损约40%  <br>目标为超越大盘和大部分公募基金</p>
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

                    <p style="font-weight:bold;
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.15);
                        margin-top: 25px;
                        padding:1%;"
                    >案例展示</p>
                    <div v-if='radio==3'>
                      <img src="../assets/cli-C-L.png" style="
                        height: 400px;
                        width: 800px;
                        "/>
                      <br>
                      <p align="left" style="font-weight:bold;
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.1);
                        margin-top: 25px;
                        padding:1%;
                        "
                      >
                      客户C低风险投资案例展示: 红线为推荐组合的收益，蓝线为客户C的历史收益<br>
                      期间收益：4.64%(9万元)——比原来提高了<font color="red">8%</font><br>
                      期间最大回撤：4.81%(10万元)——比原来降低了<font color="green">88%</font><br>
                      期间风险收益比：0.96（即总收益/最大回撤）——比原来提高了<font color="red">166%</font><br>
                      </p>
                      <img src="../assets/cli-G-L.png" style="
                        height: 400px;
                        width: 800px;
                        "/>
                      <br>
                      <p align="left" style="font-weight:bold;
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.1);
                        margin-top: 25px;
                        padding:1%;
                        "
                      >
                      客户G低风险投资案例展示: 红线为推荐组合的收益，灰线为理财产品收益<br>
                      期间收益：23.22%(139万元)——比原来提高了<font color="red">127%</font><br>
                      组合最大回撤（可能面临的最大风险）：<font color="green">4.87%</font><br>
                      </p>
                    </div>
                    
                    <div v-if='radio==6'>
                      <img src="../assets/cli-C-M.png" style="
                        height: 400px;
                        width: 800px;
                        "/>
                      <br>
                      <p align="left" style="font-weight:bold;
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.1);
                        margin-top: 25px;
                        padding:1%;
                        "
                      >
                      客户C低风险投资案例展示: 红线为推荐组合的收益，蓝线为客户C的历史收益<br>
                      期间收益：23.39%(47万元)——比原来提高了<font color="red">40%</font><br>
                      期间最大回撤：16.18%(24万元)——比原来降低了<font color="green">60%</font><br>
                      期间风险收益比：1.45（即总收益/最大回撤）——比原来提高了<font color="red">199%</font><br>
                      </p>
                      <img src="../assets/cli-G-M.png" style="
                        height: 400px;
                        width: 800px;
                        "/>
                      <br>
                      <p align="left" style="font-weight:bold;
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.1);
                        margin-top: 25px;
                        padding:1%;
                        "
                      >
                      客户G低风险投资案例展示: 红线为推荐组合的收益，灰线为理财产品收益<br>
                      期间收益：51.09%(307万元)——比原来提高了<font color="red">398%</font><br>
                      组合最大回撤（可能面临的最大风险）：<font color="green">13.49%</font><br>
                      </p>
                    </div>
                                        
                    <div v-if='radio==9'>
                      <img src="../assets/cli-C-H.png" style="
                        height: 400px;
                        width: 800px;
                        "/>
                      <br>
                      <p align="left" style="font-weight:bold;
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.1);
                        margin-top: 25px;
                        padding:1%;
                        "
                      >
                      客户C低风险投资案例展示: 红线为推荐组合的收益，蓝线为客户C的历史收益<br>
                      期间收益：55.51%(111万元)——比原来提高了<font color="red">95%</font><br>
                      期间最大回撤：14.41%(39万元)——比原来降低了<font color="green">64%</font><br>
                      期间风险收益比：3.85（即总收益/最大回撤）——比原来提高了<font color="red">365%</font><br>
                      </p>

                      <img src="../assets/cli-G-H.png" style="
                        height: 400px;
                        width: 800px;
                        "/>
                      <br>
                      <p align="left" style="font-weight:bold;
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.1);
                        margin-top: 25px;
                        padding:1%;
                        "
                      >
                      客户G低风险投资案例展示: 红线为推荐组合的收益，灰线为理财产品收益<br>
                      期间收益：59.84%(359万元)——比原来提高了<font color="red">484%</font><br>
                      组合最大回撤（可能面临的最大风险）：<font color="green">18.37%</font><br>
                      </p>

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
                    <div class="div-risk">
                      <el-radio-group v-model="hisRadio" @change="hisrecommendChange">
                        <el-radio :label="3">低风险</el-radio>
                        <el-radio :label="6">中风险</el-radio>
                        <el-radio :label="9">高风险</el-radio>
                      </el-radio-group>
                    </div>
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
      hisRadio: 3,
      // 画图
      chartData: '',
      // 画图
      PieChartOptions: {
        charts: {
          title: 'testChart'
        },
        focusTarget: 'category',
        width: 800,
        height: 480,
        is3D: true,
        pieSliceText: 'none',
        legend:{
          position: 'labeled',
          textStyle: {
            fontSize: 14,
          }
        },
        backgroundColor: 'F5F5F5',
      },  
      pieData:'',
      risked_history:'',
      risked_history_:'',
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
    // console.log('created')
  },
  components: {
    Heading
  },
  methods: {
    recommendChange(val){
      let that=this
      if(that.dateValue==undefined)
      {
      that.dateValue= ''
      that.month=''
      that.year=''
      that.historyPie=[['name', 'contribution']]
      }
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
    hisrecommendChange(vals){
      let that=this
      if (vals === 3) {
        that.risked_history_=that.chartData.history_low
      } else if (vals === 6) {
        that.risked_history_=that.chartData.history_mid
      } else if (vals === 9) {
        that.risked_history_=that.chartData.history_high
      }
      this.getRecommendCombination()
    },
    // click to get recommend combination
    getRecommendCombination() {
      for (let index = 0; index < this.risked_history_.length; index++) {
        const element = this.risked_history_[this.risked_history_.length-1-index];
        if(this.year>=element['year'] && this.month>=element['month']){
          this.historyPie=element['pieData']
          break
        }
      }
      this.historyPieDisplay=true
    },

    // date Change
    handleDateChange(value) {
      var selectedDate=new Date(value)
      this.month=selectedDate.getMonth()+1
      this.year=selectedDate.getFullYear()
      // console.log(value)
    },
    async getChartData(){
      let that=this
      // console.log('getChartData')
      this.chartData=await getChartAPI()
      // console.log(that.chartData)
      that.risked_history=that.chartData.history_low
      that.recommendPie=that.risked_history[that.risked_history.length-1]['pieData']
      // console.log(that.recommendPie)
    }
  },

}
</script>

<style scoped>
.div-bg {
  z-index: -1;
  width: 100%;
  position: fixed;
  background-image: url("../assets/1542.jpg");
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