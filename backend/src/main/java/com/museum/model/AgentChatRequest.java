package com.museum.model;

public record AgentChatRequest(
        String provinceCode,
        String provinceName,
        String message,
        String sessionId
) {
}
