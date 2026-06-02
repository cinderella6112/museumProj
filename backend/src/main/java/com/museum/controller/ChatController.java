package com.museum.controller;

import com.museum.model.AgentChatResponse;
import com.museum.model.ChatRequest;
import com.museum.model.ChatResponse;
import com.museum.model.Province;
import com.museum.service.AgentClientService;
import com.museum.service.ProvinceService;
import jakarta.validation.Valid;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Collections;
import java.util.UUID;

@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private final ProvinceService provinceService;
    private final AgentClientService agentClientService;

    public ChatController(ProvinceService provinceService, AgentClientService agentClientService) {
        this.provinceService = provinceService;
        this.agentClientService = agentClientService;
    }

    @PostMapping("/{provinceCode}")
    public ChatResponse chat(
            @PathVariable String provinceCode,
            @Valid @RequestBody ChatRequest request,
            @RequestHeader(value = "X-Session-Id", required = false) String sessionId) {

        Province province = provinceService.findByCode(provinceCode)
                .orElseThrow(() -> new IllegalArgumentException("未找到省份: " + provinceCode));

        String effectiveSessionId = sessionId != null && !sessionId.isBlank()
                ? sessionId
                : UUID.randomUUID().toString();

        AgentChatResponse agentResponse = agentClientService.chat(
                province, request.message(), effectiveSessionId);

        return new ChatResponse(
                agentResponse.reply(),
                province.code(),
                province.name(),
                agentResponse.suggestions() != null
                        ? agentResponse.suggestions()
                        : Collections.emptyList()
        );
    }
}
