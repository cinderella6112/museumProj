package com.museum.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.client.SimpleClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

@Configuration
public class AgentClientConfig {

    @Value("${museum.agent.connect-timeout-ms:5000}")
    private int connectTimeoutMs;

    @Value("${museum.agent.read-timeout-ms:120000}")
    private int readTimeoutMs;

    @Bean
    public RestTemplate agentRestTemplate() {
        SimpleClientHttpRequestFactory factory = new SimpleClientHttpRequestFactory();
        factory.setConnectTimeout(connectTimeoutMs);
        factory.setReadTimeout(readTimeoutMs);
        return new RestTemplate(factory);
    }
}
