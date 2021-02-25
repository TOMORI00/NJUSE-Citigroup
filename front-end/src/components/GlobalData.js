// 2021-2-22 mjh 全局变量

let isAuthenticated = false
let userId = -1
let userName = ''
let userPwd = ''
let isTableGot = false

// 客户追踪表的相关数据
// 客户追踪表显示数据
let testTableData = [
    {
        name: '王小虎',
        contact: '110',
        signUpTime: '2016-05-02',
        priority: {
            message: '低',
            value: 1,
        },
        nextTime: '2021-03-01',
        detail: '',
    },
    {
        name: '王小虎',
        contact: '119',
        signUpTime: '2016-05-04',
        priority: {
            message: '低',
            value: 1,
        },
        nextTime: '2021-03-01',
        detail: '',
    },
    {
        name: '王小虎',
        contact: '120',
        signUpTime: '2016-05-01',
        priority: {
            message: '低',
            value: 1,
        },
        nextTime: '2021-03-01',
        detail: '',
    },
    {
        name: '王小虎',
        contact: '114',
        signUpTime: '2016-05-03',
        priority: {
            message: '高',
            value: 3,
        },
        nextTime: '2021-03-01',
        detail: '',
    },
    {
        name: '王小虎',
        contact: '114',
        signUpTime: '2016-05-03',
        priority: {
            message: '中',
            value: 2,
        },
        nextTime: '2021-03-01',
        detail: '',
    },
    {
        name: '王小虎',
        contact: '114',
        signUpTime: '2016-05-03',
        priority: {
            message: '高',
            value: 3,
        },
        nextTime: '2021-03-01',
        detail: '',
    },
    {
        name: '王小虎',
        contact: '114',
        signUpTime: '2016-05-03',
        priority: {
            message: '低',
            value: 1,
        },
        nextTime: '2021-03-01',
        detail: '',
    },
]
// 客户追踪表添加时表单
let acctAddData = {
    name: '',
    contact: '',
    signUpTime: '',
    priority: {
        message: '',
        value: 0,
    },
    nextTime: '',
    detail: '',
}

let acctChangeData = {
    name: '',
    contact: '',
    signUpTime: '',
    priority: {
        message: '',
        value: 0,
    },
    nextTime: '',
    detail: '',
}

let acctDelData = {
    name: '',
    contact: '',
    signUpTime: '',
    priority: {
        message: '',
        value: 0,
    },
    nextTime: '',
    detail: '',
}

export default {
    isAuthenticated,
    userId,
    userName,
    userPwd,
    testTableData,
    acctAddData,
    acctChangeData,
    acctDelData,
    isTableGot,
}