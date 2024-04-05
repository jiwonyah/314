package com.Project.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import com.Project.entity.UserAccount;
import com.Project.repository.UserRepository;

@Controller
public class LoginController {
	
	@Autowired
	private UserRepository userRepository;
	
	@GetMapping("/")
	public String login() {
		return "login";
	}
	
	@PostMapping("/login")
	public String userLogin(@RequestParam("username") String username, @RequestParam("password") String password, Model model) {
		UserAccount userAccount = userRepository.findByUsername(username);
		if(userAccount!= null && userAccount.getPassword()!= null && userAccount.getPassword().equals(password)) {
			return "home";
		}else {
			model.addAttribute("error", true);
			return "login";
		}
	}
}
