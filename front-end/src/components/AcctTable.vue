2021-2-23 mjh 修改：客户追踪表组件

<template>
    <div>
        <el-table ref="multipleTable" :data="tableData"
                  stripe border height="350" highlight-current-row
                  @current-change="handleCurrentChange"
                  @selection-change="handleSelectionChange"
                  style="width: 100%">
            <el-table-column prop="name" label="姓名" width="80" sortable></el-table-column>
            <el-table-column prop="contact" label="联系方式" width="110" sortable></el-table-column>
            <el-table-column prop="signUpTime" label="注册时间" width="110" sortable></el-table-column>
            <el-table-column prop="priority.message" label="优先级" width="90" sortable
                             sort-by="priority.value"></el-table-column>
            <el-table-column prop="nextTime" label="下次联系时间" width="130" sortable></el-table-column>
            <el-table-column prop="detail" label="备注"></el-table-column>
            <el-table-column type="selection" width="50" style="display: none"></el-table-column>
        </el-table>
        <el-divider></el-divider>
        <div>
            <el-button @click="acctAddVisible=true" style="width: 100px">添加</el-button>
            <el-button @click="handleAcctChange" style="width: 100px">修改</el-button>
            <el-button @click="handleAcctDel" style="width: 100px">删除</el-button>
        </div>
        <el-dialog title="添加客户信息" :visible.sync="acctAddVisible">
            <el-form :model="acctAddData">
                <el-form-item label="客户姓名" :label-width="acctAddLabelWidth">
                    <el-input v-model="acctAddData.name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="客户联系方式" :label-width="acctAddLabelWidth">
                    <el-input v-model="acctAddData.contact" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="客户注册时间" :label-width="acctAddLabelWidth">
                    <el-date-picker
                        v-model="acctAddData.signUpTime"
                        type="date"
                        placeholder="选择日期"
                        style="float: left"
                        format="yyyy 年 MM 月 dd 日"
                        value-format="yyyy-MM-dd">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="优先级" :label-width="acctAddLabelWidth">
                    <el-select v-model="acctAddData.priority.message" placeholder="请选择优先级" style="float: left">
                        <el-option label="高" value="高"></el-option>
                        <el-option label="中" value="中"></el-option>
                        <el-option label="低" value="低"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="下次联系时间" :label-width="acctAddLabelWidth">
                    <el-date-picker
                        v-model="acctAddData.nextTime"
                        type="date" placeholder="选择日期"
                        style="float: left"
                        format="yyyy 年 MM 月 dd 日"
                        value-format="yyyy-MM-dd">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="备注" :label-width="acctAddLabelWidth">
                    <el-input v-model="acctAddData.detail" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="ackAcctAdd">确 定</el-button>
                <el-button @click="cancelAcctAdd">取 消</el-button>
            </div>
        </el-dialog>
        <el-dialog title="修改客户信息" :visible.sync="acctChangeVisible">
            <el-form :model="acctChangeData">
                <el-form-item label="客户姓名" :label-width="acctAddLabelWidth">
                    <el-input v-model="acctChangeData.name" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="客户联系方式" :label-width="acctAddLabelWidth">
                    <el-input v-model="acctChangeData.contact" autocomplete="off"></el-input>
                </el-form-item>
                <el-form-item label="客户注册时间" :label-width="acctAddLabelWidth">
                    <el-date-picker
                        v-model="acctChangeData.signUpTime"
                        type="date"
                        placeholder="选择日期"
                        style="float: left"
                        format="yyyy 年 MM 月 dd 日"
                        value-format="yyyy-MM-dd">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="优先级" :label-width="acctAddLabelWidth">
                    <el-select v-model="acctChangeData.priority.message" placeholder="请选择优先级" style="float: left">
                        <el-option label="高" value="高"></el-option>
                        <el-option label="中" value="中"></el-option>
                        <el-option label="低" value="低"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="下次联系时间" :label-width="acctAddLabelWidth">
                    <el-date-picker
                        v-model="acctChangeData.nextTime"
                        type="date" placeholder="选择日期"
                        style="float: left"
                        format="yyyy 年 MM 月 dd 日"
                        value-format="yyyy-MM-dd">
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="备注" :label-width="acctAddLabelWidth">
                    <el-input v-model="acctChangeData.detail" autocomplete="off"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="ackAcctChange">确 定</el-button>
                <el-button @click="cancelAcctChange">取 消</el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
import GlobalData from "./GlobalData";

import {getAcctTableAPI} from "../api/output";
import {acctAddAPI} from "../api/upload";
import {acctChangeAPI} from "../api/upload";
import {acctDelAPI} from "../api/upload";
import {ackSignIn} from "../api/upload";

export default {
    name: "AcctTable",
    data() {
        return {
            tableData: GlobalData.testTableData,
            currentRow: null,
            multipleSelection: [],
            acctAddVisible: false,
            acctAddData: GlobalData.acctAddData,
            acctAddLabelWidth: '100px',
            acctChangeVisible: false,
            acctChangeData: GlobalData.acctChangeData,
            acctChangeBackUp: null,
            acctDelData: GlobalData.acctDelData,
        }
    },
    methods: {
        handleCurrentChange(val) {
            this.currentRow = val;
        },
        handleSelectionChange(val) {
            this.multipleSelection = val;
        },
        async ackAcctAdd() {
            this.acctAddData.priority.value = this.priorityChange(this.acctAddData.priority.message)
            // const res = await acctAddAPI({
            //     acctData:this.acctAddData,
            //     type:'add',
            // })
            let tmpData = Object.assign({}, this.acctAddData)
            this.tableData.push(tmpData)
            this.acctAddData = ({
                name: '',
                contact: '',
                signUpTime: '',
                priority: {
                    message: '',
                    value: 0,
                },
                nextTime: '',
                detail: '',
            })
            this.acctAddVisible = false
        },
        cancelAcctAdd() {
            this.acctAddData = ({
                name: '',
                contact: '',
                signUpTime: '',
                priority: {
                    message: '',
                    value: 0,
                },
                nextTime: '',
                detail: '',
            })
            this.acctAddVisible = false
        },
        handleAcctChange() {
            if (this.multipleSelection.length > 1) {
                this.$notify.error({
                    title: '错误',
                    message: '不可一次修改多个客户信息'
                });
            } else if (this.multipleSelection.length === 1) {
                this.acctChangeData = this.multipleSelection[0]
                this.acctChangeBackUp = Object.assign({}, this.acctChangeData)
                this.acctChangeVisible = true
            } else {
                if (this.currentRow !== null) {
                    this.acctChangeData = this.currentRow
                    this.acctChangeBackUp = Object.assign({}, this.acctChangeData)
                    this.acctChangeVisible = true
                } else {
                    this.$notify.error({
                        title: '错误',
                        message: '未选择行'
                    });
                }
            }
        },
        async ackAcctChange() {
            this.acctChangeData.priority.value = this.priorityChange(this.acctChangeData.priority.message)
            // const res = await acctChangeAPI({
            //     acctData:this.acctChangeData,
            //     type:'change',
            // })
            this.acctChangeVisible = false
        },
        cancelAcctChange() {
            this.acctChangeData.name = this.acctChangeBackUp.name
            this.acctChangeData.contact = this.acctChangeBackUp.contact
            this.acctChangeData.signUpTime = this.acctChangeBackUp.signUpTime
            this.acctChangeData.priority.message = this.acctChangeBackUp.priority.message
            this.acctChangeData.priority.value = this.acctChangeBackUp.priority.value
            this.acctChangeData.nextTime = this.acctChangeBackUp.nextTime
            this.acctChangeData.detail = this.acctChangeBackUp.detail
            console.log(this.acctChangeData.detail)
            console.log(this.acctChangeBackUp.detail)
            this.acctChangeVisible = false
        },
        async handleAcctDel() {
            if (this.multipleSelection.length > 0) {
                // const res = await acctDelAPI({
                //     acctData: this.multipleSelection,
                //     type: 'multiDelete',
                // })
                for (let i = 0; i < this.multipleSelection.length; i++) {
                    this.deleteRow(this.multipleSelection[i])
                }
            } else {
                if (this.currentRow !== null) {
                    this.acctDelData = this.currentRow
                    // const res = await acctDelAPI({
                    //     acctData: this.acctDelData,
                    //     type: 'delete',
                    // })
                    this.deleteRow(this.acctDelData)
                } else {
                    this.$notify.error({
                        title: '错误',
                        message: '未选择行'
                    });
                }
            }
        },
        deleteRow(row) {
            for (let i = 0; i < this.tableData.length; i++) {
                if (row === this.tableData[i]) {
                    this.tableData.splice(i, 1)
                }
            }
        },
        priorityChange(message) {
            if (message === "高") {
                return 3
            } else if (message === "中") {
                return 2
            } else {
                return 1
            }
        },
        async getAcctTableData(){
            if(!GlobalData.isTableGot) {
                // const res = await ackSignIn(GlobalData.userName)
                // this.tableData = await getAcctTableAPI()
                GlobalData.isTableGot = true
                console.log('create')
            }
        }
    },
    components: {},
    created() {
        this.getAcctTableData()
    }
}
</script>

<style scoped>
@import url('GlobalStyle.css');
</style>