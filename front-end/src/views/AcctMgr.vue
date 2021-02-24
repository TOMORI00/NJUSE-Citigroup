2021-2-23 mjh 客户经理页面

<template>
  <div>
    <BackGround></BackGround>
    <Heading_2></Heading_2>
    <div class="div-main">
      <el-container>
        <el-aside></el-aside>
        <el-main>
          <div class="main-block">
            <el-table :data="tableData" stripe border height="330" highlight-current-row
                      @current-change="handleCurrentChange" @selection-change="handleSelectionChange"
                      style="width: 100%">
              <el-table-column prop="name" label="姓名" width="100"></el-table-column>
              <el-table-column prop="contact" label="联系方式" width="100"></el-table-column>
              <el-table-column prop="firstTime" label="注册时间" width="100"></el-table-column>
              <el-table-column prop="priority" label="优先级" width="100"></el-table-column>
              <el-table-column prop="nextTime" label="下次联系" width="100"></el-table-column>
              <el-table-column prop="detail" label="备注"></el-table-column>
              <el-table-column type="selection" width="50" style="display: none"></el-table-column>
            </el-table>
            <el-divider></el-divider>
            <div>
              <el-button type="text" @click="dialogFormVisible=true" style="width: 100px">添加</el-button>
              <el-button style="width: 100px">修改</el-button>
              <el-button style="width: 100px">删除</el-button>
            </div>
            <el-dialog title="客户信息" :visible.sync="dialogFormVisible">
              <el-form :model="acctAdd">
                <el-form-item label="客户姓名" :label-width="acctAddLabelWidth">
                  <el-input v-model="acctAdd.name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="客户联系方式" :label-width="acctAddLabelWidth">
                  <el-input v-model="acctAdd.name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="客户注册时间" :label-width="acctAddLabelWidth">
                </el-form-item>
                <el-form-item label="优先级" :label-width="acctAddLabelWidth">
                  <el-select v-model="acctAdd.region" placeholder="请选择活动区域" style="float: left">
                    <el-option label="区域一" value="shanghai"></el-option>
                    <el-option label="区域二" value="beijing"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="下次联系时间" :label-width="acctAddLabelWidth">
                </el-form-item>
                <el-form-item label="备注" :label-width="acctAddLabelWidth">
                  <el-input v-model="acctAdd.name" autocomplete="off"></el-input>
                </el-form-item>
              </el-form>
              <div slot="footer" class="dialog-footer">
                <el-button @click="dialogFormVisible = false">取 消</el-button>
                <el-button type="primary" @click="dialogFormVisible = false">确 定</el-button>
              </div>
            </el-dialog>
          </div>
          <el-divider></el-divider>
        </el-main>
        <el-aside></el-aside>
      </el-container>
    </div>
  </div>
</template>

<script>
    import BackGround from "../components/BackGround";
    import Heading_2 from "../components/Heading_2";

    import GlobalData from "../components/GlobalData";

    export default {
        name: "AcctMgr",
        data() {
            return {
                tableData: GlobalData.testTableData,
                currentRow: null,
                multipleSelection: [],
                dialogFormVisible: false,
                acctAdd: {
                    name: '',
                    region: '',
                    date1: '',
                    date2: '',
                    delivery: false,
                    type: [],
                    resource: '',
                    desc: ''
                },
                acctAddLabelWidth: '100px'
            }
        },
        methods: {
            handleCurrentChange(val) {
                this.currentRow = val;
            },
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
        },
        components: {
            BackGround,
            Heading_2,
        },
    }
</script>

<style scoped>
  @import url('../components/GlobalStyle.css');
</style>