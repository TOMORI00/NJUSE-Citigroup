import { axios } from '@/utils/request'
const api = {
    outputPre: '/api/output'
}

export function getDataAPI(){
    return axios({
        url: `${api.outputPre}/getData`,
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