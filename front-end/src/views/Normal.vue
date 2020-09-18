<template>
  <div class="div-main">
    <!--    1-->
    <heading></heading>

    <!--    3-->
    <el-container id="my-container">
      <el-header height="40px" style="margin: 20px">
        <el-select v-model="value" @change="handleTypeChange">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-header>

      <!--      4-->
      <el-upload id="importExcel" drag action="#" multiple :on-change="handleChange" :on-preview="handlePreview"
                 :before-remove="beforeRemove" :on-remove="handleRemove" :file-list="fileList" :auto-upload="false">
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">（只能上传Excel文件）</div>
      </el-upload>
      <br>
      <el-button id="upload-ack" @click="uploadAck" style="margin: auto;width:73.9px;height: 39.6px">确 认</el-button>
      <el-divider></el-divider>

      <!--      5-->
      <div class="div-result" id="div-result" style="display: none">

        <!--        8-->
        <p style="margin: 20px">Recommend</p>
        <GChart class="analysis-chart" type="LineChart" :data=chartData :options="chartOption"/>
        <span>开始时间   </span>
        <el-date-picker v-model="dateValue" type="month" format="yyyy年MM月" placeholder="选择开始时间"
                        @change="handleDateChange"></el-date-picker>
        <br>
        <el-button @click="getRecommendCombination" style="margin-top: 20px">生成历史推荐组合</el-button>


        <el-divider></el-divider>

        <!--        9-->
        <el-button @click="getReport">一键生成报告</el-button>
        <el-button @click="toHome">HomePage</el-button>
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
                // 切换场内场外的选项
                value: 'inside',
                options: [{
                    value: 'inside',
                    label: '场内'
                }, {
                    value: 'outside',
                    label: '场外'
                }],

                // 上传的文件列表
                fileList: [],

                currentType: 'none',

                // 画图
                chartData: [
                    ['x-line', 'number1', 'number2'],
                    [20, 25, 30],
                    [25, 40, 56],
                    [30, 56, 24]
                ],
                // 画图
                chartOption: {
                    charts: {
                        title: 'testChart'
                    },
                    focusTarget: 'category'
                },
                // 开始日期
                dateValue: '',

                //
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

            // 隐藏选择界面进入具体界面
            clickToInit() {
                this.value = this.currentType
            },

            // 设置场内相关数据
            clickToInside() {
                this.currentType = 'inside'
                document.getElementById('div-risk').style.display = "none"
                this.clickToInit()
            },

            // 设置场外相关数据
            clickToOutSide() {
                this.currentType = 'outside'
                this.clickToInit()
            },

            // 修改场内场外类型
            handleTypeChange(value) {
                this.currentType = value
                console.log('handleTypeChange')
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

            // 确定导入完成后发送数据
            uploadAck() {
                if (this.fileList.length > 0) {
                    document.getElementById('div-result').style.display = 'unset'
                    const data = {
                        jsonString: JSON.stringify(this.allFile)
                    }
                    const res = importExcelAPI(data)
                } else {
                    this.$message({
                        message: '请上传文件！',
                        type: 'warning'
                    });
                }
            },

            // 网上找的JS读取Excel文件的方法
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

            // click to get report
            getReport() {
                console.log('getReport')
            },

            // click to get recommend combination
            getRecommendCombination() {
                console.log('getRecommendCombination')
            },

            // date Change
            handleDateChange(value) {
                console.log(value)
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