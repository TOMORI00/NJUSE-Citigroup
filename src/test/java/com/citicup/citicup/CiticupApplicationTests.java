package com.citicup.citicup;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class CiticupApplicationTests {

    @Test
    void contextLoads() {
        JSONArray jsonArray = JSONObject.parseArray("[{\"a\":1,\"b\":2},[2,3]]");
        System.out.println("Done!");
    }

}
