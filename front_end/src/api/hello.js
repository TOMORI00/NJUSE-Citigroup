import { axios } from '@/utils/request'
const api = {
    helloPre: '/api/hello'
}

export function getAPI(){
    return axios({
        url: `${api.helloPre}/get`,
        method: 'POST',
    })
}

export function postAPI(data){
    console.log(data)
    return axios({
        url: `${api.helloPre}/post`,
        method: 'POST',
        data,
    })
}