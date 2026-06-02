package com.museum.model;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

public record ChatRequest(
        @NotBlank(message = "消息内容不能为空")
        @Size(max = 4000, message = "消息长度不能超过4000字符")
        String message
) {
}
