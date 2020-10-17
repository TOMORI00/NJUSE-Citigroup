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

