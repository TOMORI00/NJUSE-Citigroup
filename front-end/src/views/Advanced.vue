此页为专业用户页，是银行经理使用的页面
- 本页元素与交互
- 图片背景
- 左上图标》跳转至某页面（目前为主页）
- 右上软件名称
- 中央
- 理财、基金选择框
- excel上传
- 功能页
- 复现
- 历史复现
- 对比复现
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
            <el-tabs v-model="activeTab">

              <el-tab-pane label="投资记录上传" name="first" v-if='!uploaded'>

                <el-container id="my-container">
                  <el-header height="40px" style="margin: 20px">
                    <el-select v-model="type" @change="handleTypeChange">
                      <el-option v-for="item in options" :key="item.value" :label="item.label"
                                 :value="item.value"></el-option>
                    </el-select>
                  </el-header>
                </el-container>

                <el-upload id="importExcel" drag action="#" multiple :on-change="handleChange"
                           :on-preview="handlePreview"
                           :before-remove="beforeRemove" :on-remove="handleRemove" :file-list="fileList"
                           :auto-upload="false">
                  <i class="el-icon-upload"></i>
                  <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
                  <div class="el-upload__tip" slot="tip">（只能上传Excel文件）</div>
                </el-upload>
                <br>
                <el-button id="upload-ack" @click="uploadAck" style="margin: auto;width:73.9px;height: 39.6px">确 认
                </el-button>

              </el-tab-pane>

              <el-tab-pane label="投资复现" name="second" v-if='uploaded'>

                <div class="div-analysis">
                  <p style="font-weight:bold;
                          font-size:20px;
                          border-radius: 15px;
                          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                          background: rgba(0, 0, 0, 0.2);
                          margin-top: 25px;
                          padding:1%;"
                  >历史复现</p>
                  <div style="width: 800px;height: 480px;margin: auto">
                  <GChart type="LineChart" :data=historyLine :options="LineChartOptions"/>
                  </div>
                </div>

                <el-divider></el-divider>

                <div class="div-analysis">
                  <p style="font-weight:bold;
                          font-size:20px;
                          border-radius: 15px;
                          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                          background: rgba(0, 0, 0, 0.2);
                          margin-top: 25px;
                          padding:1%;"
                  >对比复现</p>
                  <div class="div-risk">
                    <el-radio-group v-model="compRadio" @change="compareLineChange">
                      <el-radio :label="3">低风险</el-radio>
                      <el-radio :label="6">中风险</el-radio>
                      <el-radio :label="9">高风险</el-radio>
                    </el-radio-group>
                  </div>
                  <div style="width: 800px;height: 480px;margin: auto">
                  <GChart type="LineChart" :data=compareLine :options="LineChartOptions"/>
                  </div>

                </div>

                <!-- 备用的修改基金池功能 -->
                <!-- <el-button @click="changeFund" v-if="false">修改基金池</el-button>
                <el-dialog title="修改基金池" :visible.sync="dialogVisible" width="30%">
                <span>修改基金池细节</span>
                <span slot="footer" class="dialog-footer">
                <el-button @click="dialogVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
                </span>
                </el-dialog> -->
              </el-tab-pane>

              <el-tab-pane label="投资建议" name="third" v-if='uploaded'>

                <p style="font-weight:bold;
                          font-size:20px;
                          border-radius: 15px;
                          box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                          background: rgba(0, 0, 0, 0.2);
                          margin-top: 25px;
                          padding:1%;"
                >投资建议</p>
                <div class="div-risk">
                  <el-radio-group v-model="recRadio" @change="recommendChange">
                    <el-radio :label="3">低风险</el-radio>
                    <el-radio :label="6">中风险</el-radio>
                    <el-radio :label="9">高风险</el-radio>
                  </el-radio-group>
                </div>

                <div style="width: 800px;height: 480px;margin: auto">
                <GChart type="PieChart" :data=recommendPie :options="PieChartOptions"/>
                </div>

                <el-divider></el-divider>

                <p style="font-weight:bold;
                        font-size:20px;
                        border-radius: 15px;
                        box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.2);
                        background: rgba(0, 0, 0, 0.2);
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
          </div>
          <el-divider></el-divider>
        </el-main>
        <el-aside></el-aside>
      </el-container>

      <div>{{ loading }}</div>
    </div>
  </div>
</template>

<script>
import Heading from "../components/Heading";
import XLSX from 'xlsx'
import {importExcelAPI} from "@/api/upload";
import {uploadAPI} from "@/api/upload";
import {getFvDataAPI} from "@/api/output";
import {getFpvDataAPI} from "@/api/output";
import {getChartAPI} from "@/api/output";

export default {
  name: "Advanced",
  data() {
    return {
      // 切换基金理财的选项
      type: '基金',
      options: [{
        value: '基金',
        label: '基金'
      }, {
        value: '理财',
        label: '理财'
      }],

      //默认先上传文件
      activeTab: 'first',
      uploaded: false,

      // 上传的文件列表
      fileList: [],

      // 画图
      historyLine: '',
      compareLine: '',
      recommendPie: [
        ['name', 'contribution']
      ],
      historyPie: [
        ['name', 'contribution']
      ],


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
      // 后端返回的数据
      outputData: {
        "date": '',
        "chart1": '',
        "in1": '',

        "duration": '',

        "chart2_high": '',
        "chart2_mid": '',
        "chart2_low": '',

        "chartadd2_high": '',
        "chartadd2_mid": '',
        "chartadd2_low": '',

        "in2_high": '',
        "in2_mid": '',
        "in2_low": ''
      },
      LineChartOptions: {
        charts: {
          title: 'testChart'
        },
        focusTarget: 'category',
        width: 800,
        height: 480,
        is3D: true,
        colors:['red','blue']
      },

      // 修改基金池
      dialogVisible: false,
      // 对比复现风险
      compRadio: 3,
      // 推荐组合风险
      recRadio: 3,
      hisRadio: 3,
      chartData: '',
      risked_history:'',
      hisrisked_history:'',
      // 开始日期
      dateValue: '',
      month:'',
      year:'',
      // 历史推荐组合饼图显示与否
      historyPieDisplay:false,

      loading:'',

      // 文件
      current: {
        name: "",
        content: {}
      },
      allFile: {},
    }
  },
  components: {
    Heading
  },
  methods: {
    // 返回首页
    toHome() {
      this.$router.back()
    },

    // 修改场内场外类型
    handleTypeChange(value) {
      // console.log(value)
    },

    // 确定导入完成后发送数据
    async uploadAck() {
      let that = this
      if (this.fileList.length > 0) {
        that.loading='正在计算...'
        let fd = new FormData();
        fd.append('type', that.type)
        console.log(that.type)
        this.fileList.forEach(item => {
          //文件信息中raw才是真的文件
          fd.append("files", item.raw);
          console.log(item.raw)
        })
        console.log(fd)
        const res = await uploadAPI(fd)
        if (that.type == '基金') {
          that.outputData = await getFvDataAPI()
        } else if (that.type == '理财') {
          that.outputData = await getFpvDataAPI()
        }
        console.log(that.outputData)

        that.historyLine=that.outputData.chart1
        that.compareLine=that.outputData.chart2_low

        that.chartData=await getChartAPI()
        console.log(that.chartData)

        that.risked_history=that.chartData.history_low
        that.recommendPie=that.risked_history[that.risked_history.length-1]['pieData']
        console.log(that.recommendPie)

        that.loading=''
        this.activeTab = 'second'
        this.uploaded = true

      } else {
        this.$message({
          message: '请上传文件！',
          type: 'warning'
        });
      }
    },
    // :on-change
    // 检查和导入Excel文件
    handleChange(file) {
      const fileNameInfo = file.name.split('.')
      const type = fileNameInfo[fileNameInfo.length - 1]
      const fileType = ['xlsx', 'xlc', 'xlm', 'xls', 'xlt', 'xlw', 'csv'].some(item => item === type)
      this.fileList.push(file)
      for (let i = 0; i < this.fileList.length - 1; i++) {
        if (file.name === this.fileList[0].name) {
          this.fileList.pop()
          this.$message("重复上传！请重新选择")
          return
        }
      }
      if (!fileType) {
        this.fileList.pop()
        this.$message('格式错误！请重新选择')
        return
      }
      this.fileToExcel(file).then(tabJson => {
        if (tabJson && tabJson.length > 0) {
          this.current.name = file.name
          this.current.content = tabJson
          this.allFile[this.current.name] = this.current.content
        }
      })
    },

    // :on-preview
    handlePreview(file) {
      console.log(file)
    },

    // :before-remove
    beforeRemove(file, fileList) {
      return this.$confirm(`确定移除 ${file.name}？`);
    },

    // :on-remove
    handleRemove(file, fileList) {
      this.fileList.splice(this.fileList.indexOf(file), 1)
    },

    // 读取Excel文件

    fileToExcel(file) {
      return new Promise(function (resolve, reject) {
        const reader = new FileReader()
        reader.onload = function (e) {
          const data = e.target.result
          this.wb = XLSX.read(data, {
            type: 'binary'
          })
          const result = []
          this.wb.SheetNames.forEach((sheetName) => {
            result.push({
              sheetName: sheetName,
              sheet: XLSX.utils.sheet_to_json(this.wb.Sheets[sheetName])
            })
          })
          resolve(result)
        }
        reader.readAsBinaryString(file.raw)
      })
    },

    // click to change fund
    // changeFund() {
    //     this.dialogVisible = true
    // },

    // click to get recommend combination
    getRecommendCombination() {
      for (let index = 0; index < this.hisrisked_history.length; index++) {
        const element = this.hisrisked_history[this.hisrisked_history.length-1-index];
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

    //
    compareLineChange(val) {
      let that = this
      if (val === 3) {
        that.compareLine = that.outputData.chart2_low
      } else if (val === 6) {
        that.compareLine = that.outputData.chart2_mid
      } else if (val === 9) {
        that.compareLine = that.outputData.chart2_high
      }
    },

    recommendChange(val){
      let that=this
      if (that.dateValue==undefined)
      {
        that.dateValue= ''
        that.month=''
        that.year=''
        that.historyPieDisplay=false
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
      that.historyPie=[['name', 'contribution']]
      if (vals === 3) {
        that.hisrisked_history=that.chartData.history_low
      } else if (vals === 6) {
        that.hisrisked_history=that.chartData.history_mid
      } else if (vals === 9) {
        that.hisrisked_history=that.chartData.history_high
      }
      this.getRecommendCombination()
    }

  },

}
</script>

<style>

.el-tabs__item.is-active {
  color: rgb(0, 0, 0);
  padding: 2%;
  border-radius: 5px;
  font-size: 18px;
}

.el-tabs__item {
  font-weight: bold;
  font-size: 15px;
}

.el-tabs__active-bar {
  background-color: rgb(0, 0, 0);
}

.el-radio {
  font-weight: bold;
}

</style>

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