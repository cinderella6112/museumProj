package com.museum.model;

import java.util.List;

public record AgentChatResponse(
        String reply,
        List<String> suggestions
) {
}
