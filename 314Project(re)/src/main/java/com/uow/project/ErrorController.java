package com.uow.project;

import org.springframework.web.bind.annotation.GetMapping;

public class ErrorController {
    @GetMapping("/guesterror")
    public String guestError() {
        return "guestAlert"; // 401 Unauthorized 오류 페이지 템플릿
    }
}
