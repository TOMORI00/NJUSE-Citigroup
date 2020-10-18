import {
    getDataAPI,
    getChartAPI,
    getPDFAPI
} from '@/api/output'

import {
    importExcelAPI
} from '@/api/upload'

const methods = {
    state:{
        excelData:{},
        returnData:{}
    },
    mutations:{
        setExcelData:function({state,data}){
            state.excelData = data
        },
        setReturnData:function({state,data}){
            state.returnData = data
        }
    },
    actions:{
        uploadExcel:async({state,commit})=>{
            const res = await importExcelAPI(state.excelData)
            if(res){
                commit('setReturnData',res)
            }
        }
    }
}

export default methods