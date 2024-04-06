package com.example.demo.user;


import jakarta.validation.Valid;

import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Controller
@RequestMapping("/agent")
public class AgentController {
    private final UserService userService;

    @GetMapping("/signup")
    public String signup(UserCreateForm agentCreateForm) {
        return "agent_signup_form";
    }

    @PostMapping("/signup")
    public String signup(@Valid UserCreateForm agentCreateForm, BindingResult bindingResult) {
        if (bindingResult.hasErrors()) {
            return "agent_signup_form";
        }

        if (!agentCreateForm.getPassword1().equals(agentCreateForm.getPassword2())) {
            bindingResult.rejectValue("password2", "passwordInCorrect", 
                    "2개의 패스워드가 일치하지 않습니다.");
            return "agent_signup_form";
        }

        userService.create(agentCreateForm.getUsername(), 
                Role.AGENT, agentCreateForm.getPassword1());

        return "redirect:/";
    }
    
    @GetMapping("/login")
    public String login() {
        return "agent_login_form";
    }
}
