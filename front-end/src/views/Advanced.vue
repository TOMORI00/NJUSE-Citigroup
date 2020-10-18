此页为专业用户页，是银行经理使用的页面
- 本页元素与交互
  - 图片背景
  - 左上图标》跳转至某页面（目前为NJU主页）
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
  <div class="div-main">

    <heading></heading>

    <!-- 选择基金/理财 -->
    <el-container id="my-container">
      <el-header height="40px" style="margin: 20px">
        <el-select v-model="value" @change="handleTypeChange">
          <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value"></el-option>
        </el-select>
      </el-header>
    </el-container>

    <el-tabs v-model="activeName" @tab-click="handleClick">
        
        <el-tab-pane label="文件上传" name="first">

            <el-upload id="importExcel" drag action="#" multiple :on-change="handleChange" :on-preview="handlePreview" :before-remove="beforeRemove" :on-remove="handleRemove" :file-list="fileList" :auto-upload="false">
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">（只能上传Excel文件）</div>
        </el-upload>
        <br>
        <el-button id="upload-ack" @click="uploadAck" style="margin: auto;width:73.9px;height: 39.6px">确 认</el-button>

        </el-tab-pane>

        <el-tab-pane label="投资复现" name="second">

            <div class="div-analysis">
            <p style="margin: 20px">历史复现</p>
            <GChart class="analysis-chart" type="LineChart" :data=chartData :options="chartOption"/>
            </div>
            <div class="div-analysis">
            <p style="margin: 20px">对比复现</p>
            <GChart class="analysis-chart" type="LineChart" :data=chartData :options="chartOption"/>
            </div>

            <!-- 备用的修改基金池功能 -->
            <el-button @click="changeFund" v-if="false">修改基金池</el-button>
            <el-dialog title="修改基金池" :visible.sync="dialogVisible" width="30%">
            <span>修改基金池细节</span>
            <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="dialogVisible = false">确 定</el-button>
            </span>
            </el-dialog>

        </el-tab-pane>

        <el-tab-pane label="投资建议" name="third">

                    <p>投资建议</p>
                    <div class="div-risk" id="div-risk">
                        <el-radio-group v-model="radio">
                        <el-radio :label="3">低风险</el-radio>
                        <el-radio :label="6">中风险</el-radio>
                        <el-radio :label="9">高风险</el-radio>
                        </el-radio-group>
                    </div>
                    <GChart class="analysis-chart" type="LineChart" :data=chartData :options="chartOption"/>
                    
                    <p style="margin: 20px">历史推荐</p>
                    <span>开始时间   </span>
                    <el-date-picker v-model="dateValue" type="month" format="yyyy年MM月" placeholder="选择开始时间"
                                    @change="handleDateChange"></el-date-picker>
                    <br>
                    <el-button @click="getRecommendCombination" style="margin-top: 20px">历史推荐</el-button>
        </el-tab-pane>
        
    </el-tabs>
    <el-divider></el-divider>

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
                // 切换基金理财的选项
                value: '基金',
                options: [{
                    value: 'fundation',
                    label: '基金'
                }, {
                    value: 'financing',
                    label: '理财'
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

                // 对比复现
                checked: false,
                // 修改基金池
                dialogVisible: false,
                // 风险
                radio: 3,
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
                document.getElementById('div-choose').style.display = "none"
                document.getElementById('my-container').style.display = "unset"
                this.value = this.currentType
            },

            // 设置基金相关数据
            clickToInside() {
                this.currentType = 'fundation'
                document.getElementById('div-risk').style.display = "none"
                this.clickToInit()
            },

            // 设置理财相关数据
            clickToOutSide() {
                this.currentType = 'financing'
                this.clickToInit()
            },

            // 修改场内场外类型
            handleTypeChange(value) {
                this.currentType = value
                if (value === 'inside') {
                    document.getElementById('div-risk').style.display = "none"
                } else {
                    document.getElementById('div-risk').style.display = "unset"
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

            // checkbox change
            changeCheckBox(check) {
                console.log(check)
            },

            // click to change fund
            changeFund() {
                this.dialogVisible = true
            },

            // click to get recommend
            getRecommend() {
                document.getElementById('div-recommend').style.display = "unset"
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

  #div-choose {
    border-radius: 15px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    width: 800px;
    height: 450px;
    background: white;
    margin-top: 75px;
    margin-left: auto;
    margin-right: auto;
  }

  .choose-button {
    margin: 50px;
    width: 200px;
    height: 200px;
    position: relative;
    top: 65px;
  }

  .analysis-chart {
    width: 960px;
    height: 480px;
    margin: auto;
  }
</style>