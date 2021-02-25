import {axios} from "@/utils/request";

const api = {
    importExcel: '/api/upload'
}

export function importExcelAPI(data) {
    return axios({
        url: `${api.importExcel}/importExcel`,
        method: 'post',
        data
    })
}

export function uploadAPI(data) {
    return axios({
        url: `${api.importExcel}/uploadExcel`,
        method: 'post',
        data
    })
}


// 2021-2-24 mjh 登录API
// 向后端发送登录信息：用户名、密码
// 要求返回登录验证结果
export function signInAPI(data) {
    return axios({
        url: `${api.importExcel}/signIn`,
        method: 'post',
        data,
    })
}

// 2021-2-24 mjh 注册API
// 向后端发送注册信息：用户名、密码
// 要求返回注册验证结果
export function signUpAPI(data) {
    return axios({
        url: `${api.importExcel}/signUp`,
        method: 'post',
        data,
    })
}

// 2021-2-25 mjh 客户追踪表添加API
// 向后端发送客户追踪表信息
export function acctAddAPI(data){
    return axios({
        url: `/api/upload/acctAdd`,
        method: 'post',
        data,
    })
}

// 2021-2-25 mjh 客户追踪表修改API
// 向后端发送客户追踪表信息
export function acctChangeAPI(data){
    return axios({
        url: `/api/upload/acctChange`,
        method: 'post',
        data,
    })
}

// 2021-2-25 mjh 客户追踪表删除API
// 向后端发送客户追踪表信息
export function acctDelAPI(data){
    return axios({
        url: `/api/upload/acctDel`,
        method: 'post',
        data,
    })
}

// 2021-2-25 mjh 客户追踪表查询API
// 向后端发送当前登录用户信息，主要为用户名
export function ackSignIn(data){
    return axios({
        url: `/api/upload/ackSignUp`,
        method:'post',
        data
    })
}