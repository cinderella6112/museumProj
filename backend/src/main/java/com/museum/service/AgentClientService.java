package com.museum.service;

import com.museum.model.AgentChatRequest;
import com.museum.model.AgentChatResponse;
import com.museum.model.Province;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

@Service
public class AgentClientService {

    private static final Logger log = LoggerFactory.getLogger(AgentClientService.class);

    private final RestTemplate restTemplate;
    private final String agentBaseUrl;

    public AgentClientService(
            RestTemplate agentRestTemplate,
            @Value("${museum.agent.base-url}") String agentBaseUrl) {
        this.restTemplate = agentRestTemplate;
        this.agentBaseUrl = agentBaseUrl.endsWith("/")
                ? agentBaseUrl.substring(0, agentBaseUrl.length() - 1)
                : agentBaseUrl;
    }

    public AgentChatResponse chat(Province province, String message, String sessionId) {
        String url = agentBaseUrl + "/api/v1/chat";
        AgentChatRequest body = new AgentChatRequest(
                province.code(),
                province.name(),
                message,
                sessionId
        );

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<AgentChatRequest> entity = new HttpEntity<>(body, headers);

        try {
            ResponseEntity<AgentChatResponse> response = restTemplate.postForEntity(
                    url, entity, AgentChatResponse.class);
            if (response.getBody() == null) {
                throw new AgentUnavailableException("智能体返回空响应");
            }
            return response.getBody();
        } catch (RestClientException ex) {
            log.error("调用 Python 智能体失败: province={}, url={}", province.code(), url, ex);
            throw new AgentUnavailableException("智能体服务暂不可用，请确认 Python 服务已启动", ex);
        }
    }
}
