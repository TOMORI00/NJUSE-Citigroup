import { axios } from '@/utils/request'
const api = {
    outputPre: '/api/output'
}

// 获取基金数据
export function getFvDataAPI(){
    return axios({
        url: `${api.outputPre}/getFvData`,
        method: 'GET'
    })
}

// 获取理财数据
export function getFpvDataAPI(){
    return axios({
        url: `${api.outputPre}/getFpvData`,
        method: 'GET'
    })
}

export function getChartAPI(){
    return axios({
        url: `${api.outputPre}/getChart`,
        method: 'GET'
    })
}

export function getPDFAPI(){
    return axios({
        url: `${api.outputPre}/getPDF`,
        method: 'GET'
    })
}

// 2021-2-25 mjh 前端获取客户追踪表信息API
export function getAcctTableAPI(){
    return axios({
        url: `/api/output/getAcctTable`,
        method:'GET',
    })
}