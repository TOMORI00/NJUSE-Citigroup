package com.citicup.citicup.config;

import org.springframework.web.filter.CorsFilter;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

/**
 * @author 山山
 * @date 2020-09-03
 */

@Configuration
public class CorsConfig {

    /**
     * 允许跨域请求的站点
     */
    private static String[] originsVal = new String[]{
            "localhost:8000",
            "127.0.0.1:8000",
            "127.0.0.1",
            "localhost",
            "172.19.144.143",
            "172.19.144.143:8000"
    };

    @Bean
    public CorsFilter corsFilter() {
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        CorsConfiguration corsConfiguration = new CorsConfiguration();
        addAllowedOrigins(corsConfiguration);
        corsConfiguration.addAllowedHeader("*");
        corsConfiguration.addAllowedMethod("*");
        corsConfiguration.setAllowCredentials(true);
        source.registerCorsConfiguration("/**", corsConfiguration);
        return new CorsFilter(source);
    }

    private void addAllowedOrigins(CorsConfiguration corsConfiguration) {
        for (String origin : originsVal) {
            corsConfiguration.addAllowedOrigin("http://" + origin);
            corsConfiguration.addAllowedOrigin("https://" + origin);
        }
    }
}
