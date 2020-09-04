package com.citicup.citicup.bl.upload;

import com.citicup.citicup.VO.ResponseVO;

import java.util.ArrayList;
import java.util.Dictionary;

public interface UploadService {
    ResponseVO importExcel(String jsonString);
}
