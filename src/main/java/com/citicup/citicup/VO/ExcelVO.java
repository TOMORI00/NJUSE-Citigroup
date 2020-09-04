package com.citicup.citicup.VO;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONObject;

public class ExcelVO {
    private String jsonString;
    private JSONObject jsonObject;

    public void stringToJson(){
        jsonObject = JSONObject.parseObject(jsonString);
    }

    public void setJsonObject(JSONObject jsonObject) {
        this.jsonObject = jsonObject;
    }

    public void setJsonString(String jsonString) {
        this.jsonString = jsonString;
    }

    public JSONObject getJsonObject() {
        return jsonObject;
    }

    public String getJsonString() {
        return jsonString;
    }
}
