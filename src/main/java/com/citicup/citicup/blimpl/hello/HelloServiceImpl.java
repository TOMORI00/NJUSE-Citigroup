package com.citicup.citicup.blimpl.hello;

import com.citicup.citicup.VO.ResponseVO;
import com.citicup.citicup.bl.hello.HelloService;
import org.springframework.stereotype.Service;

@Service
public class HelloServiceImpl implements HelloService {

    @Override
    public int get() {
        return 2020;
    }

    @Override
    public ResponseVO post(int i) {
        System.out.println("post成功："+i);
        return ResponseVO.buildSuccess(i);
    }
}
