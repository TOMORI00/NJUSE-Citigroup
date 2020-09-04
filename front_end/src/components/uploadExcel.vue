<template>
  <div>
    <el-upload
        id="importExcel"
        drag
        action="#"
        multiple
        :on-change="handleChange"
        :on-preview="handlePreview"
        :before-remove="beforeRemove"
        :on-remove="handleRemove"
        :file-list="fileList"
        :auto-upload="false">
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div class="el-upload__tip" slot="tip">（只能上传Excel文件）</div>
    </el-upload>
    <br>
    <el-button id="upload-ack" @click="uploadAck">确 认</el-button>
  </div>
</template>

<script>
import XLSX from 'xlsx'
import {importExcelAPI} from "@/api/upload";

export default {
  data() {
    return {
      fileList: [],
      current: {
        name: "",
        content: {}
      },
      allFile: [],
    }
  },
  methods: {
    // :on-change
    // 检查和导入Excel文件
    handleChange(file) {
      const tempList = this.fileList
      const fileNameInfo = file.name.split('.')
      const type = fileNameInfo[fileNameInfo.length - 1]
      const fileType = ['xlsx', 'xlc', 'xlm', 'xls', 'xlt', 'xlw', 'csv'].some(item => item === type)
      this.fileList.push(file)
      if (fileType) {
        console.log(true)
      } else {
        this.fileList.pop()
        this.$message('格式错误！请重新选择')
        console.log(false)
        return null
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
      console.log(file, fileList);
    },

    // 确定导入完成后发送数据
    uploadAck() {
      console.log(this.allFile)
      console.log([{a: 1, b: 2}, [2, 3]])
      const data = {
        jsonString: JSON.stringify({a: [{a: 1, b: 2}, [2, 3]]})
      }
      console.log(data.jsonString)
      const res = importExcelAPI(data)
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
    }
  }
}
</script>

<style></style>