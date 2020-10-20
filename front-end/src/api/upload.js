import {axios} from "@/utils/request";

const api = {
    importExcel: '/api/upload'
}

export function importExcelAPI(data){
    return axios({
        url:`${api.importExcel}/importExcel`,
        method:'post',
        data
    })
}

export function uploadAPI(data){
    return axios({
        url:`${api.importExcel}/uploadExcel`,
        method:'post',
        data
    })
}

