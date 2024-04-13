package com.example.demo;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class MainController {
	@GetMapping("/home")
	public String index() {
		return "homepage";
	}
	
    @GetMapping("/")
    public String root() {
        return "redirect:/home";
    }
}
