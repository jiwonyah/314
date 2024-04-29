package com.uow.project;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MainController {
    @GetMapping("/")
    public String home() {
        return "homepage";
    }

    
    @GetMapping("/signup")
    public String signup() {
        return "signup";
    }
    
    @GetMapping("/adminPage")
    public String admin() {
        return "admin_page";
    }
    
}
