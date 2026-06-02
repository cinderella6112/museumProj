package com.museum.model;

import java.util.List;

public record ChatResponse(
        String reply,
        String provinceCode,
        String provinceName,
        List<String> suggestions
) {
}
