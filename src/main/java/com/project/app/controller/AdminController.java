package com.project.app.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

import com.project.app.entity.User;
import com.project.app.entity.UserAccountDTO;
import com.project.app.entity.UserProfileDTO;
import com.project.app.repository.UserRepositoryAdmin;

@Controller
public class AdminController {
	
	@Autowired
	private UserRepositoryAdmin repo;
	
	@GetMapping("/user_account/dashboard")
	public String showUserAccountDashboardPage() {
		return "user_account_dashboard";
	}
	
	@GetMapping("/user_profile/dashboard")
	public String showUserProfileDashboardPage() {
		return "user_profile_dashboard";
	}

	@GetMapping("/create/user_profile")
	public String showCreateUserProfilePage(Model model) {
		UserProfileDTO userProfileDTO = new UserProfileDTO();
		model.addAttribute("userProfileDTO", userProfileDTO);
		return "create_user_profile";
	}
	
	@PostMapping("/create/user_profile")
	 public String createUserProfile(@ModelAttribute("userProfileDTO") UserProfileDTO userProfileDTO) {
		 User user = new User();
		 user.setDob(userProfileDTO.getDob());
		 user.setEmail(userProfileDTO.getEmail());
		 user.setFullName(userProfileDTO.getFullName());
		 user.setPassword(userProfileDTO.getPassword());
		 user.setRole(userProfileDTO.getRole());
		 user.setUsername(userProfileDTO.getUsername());
		 user.setAddress(userProfileDTO.getAddress());
		 user.setPhoneNumber(userProfileDTO.getPhoneNumber());
		 repo.save(user);
	        return "redirect:/user_profile/dashboard";
	    }
	
	@GetMapping("/create/user_account")
	public String showCreateUserAccountPage(Model model) {
		UserAccountDTO userAccountDTO = new UserAccountDTO();
		model.addAttribute("userAccountDTO", userAccountDTO);
		return "create_user_account";
	}
	
	@PostMapping("/create/user_account")
	public String createUserAccount(@ModelAttribute("userAccountDTO") UserAccountDTO userAccountDTO) {
		User user = new User();
		user.setFullName(userAccountDTO.getFullName());
		user.setDob(userAccountDTO.getDob());
		user.setEmail(userAccountDTO.getEmail());
		user.setUsername(userAccountDTO.getUsername());
		user.setPassword(userAccountDTO.getPassword());
		repo.save(user);
		return "redirect:/user_account/dashboard";
	}
	
	
	
}
