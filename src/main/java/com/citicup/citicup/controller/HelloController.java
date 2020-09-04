package com.citicup.citicup.controller;

import com.citicup.citicup.VO.HelloVO;
import com.citicup.citicup.VO.ResponseVO;
import com.citicup.citicup.bl.hello.HelloService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController()
@RequestMapping("/api/hello")
public class HelloController {

    @Autowired
    HelloService helloService;

    @GetMapping("/get")
    public int getFromBackend() {
        return helloService.get();
    }

    @PostMapping("/post")
    public ResponseVO postToBackend(@RequestBody HelloVO helloVO) {
        return helloService.post(helloVO.getI());
    }
}
