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