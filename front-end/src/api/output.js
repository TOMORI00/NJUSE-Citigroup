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