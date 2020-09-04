package com.citicup.citicup.controller;

import com.citicup.citicup.VO.ExcelVO;
import com.citicup.citicup.VO.ResponseVO;
import com.citicup.citicup.bl.upload.UploadService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController()
@RequestMapping("/api/upload")
public class UploadController {
    @Autowired
    UploadService uploadService;

    @PostMapping("/importExcel")
    public ResponseVO importExcel(@RequestBody ExcelVO excelVO){
        excelVO.stringToJson();
        return uploadService.importExcel(excelVO.getJsonString());
    }
}
