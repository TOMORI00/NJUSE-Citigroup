package com.citicup.citicup.blimpl.upload;

import com.citicup.citicup.VO.ResponseVO;
import com.citicup.citicup.bl.upload.UploadService;
import org.springframework.stereotype.Service;
import java.util.ArrayList;
import java.util.Dictionary;

@Service
public class UploadServiceImpl implements UploadService {

    @Override
    public ResponseVO importExcel(String jsonString) {
        System.out.println(jsonString);
        return ResponseVO.buildSuccess(jsonString);
    }
}
