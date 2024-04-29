package com.uow.project.user;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;

import org.springframework.dao.DataIntegrityViolationException;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;



@RequiredArgsConstructor
@Controller
public class UserController {

	private final UserService userService;
    private final AuthenticationManager authenticationManager;
    private final CustomUserDetailsService customUserDetailsService;

	@GetMapping("/user/signup")
	public String usersignup(UserCreateForm userCreateForm) {
		return "user_signup_form";
	}

	@PostMapping("/user/signup")
	public String signup(@Valid UserCreateForm userCreateForm, BindingResult bindingResult) {
		if (bindingResult.hasErrors()) {
			return "user_signup_form";
		}

		if (!userCreateForm.getPassword1().equals(userCreateForm.getPassword2())) {
			bindingResult.rejectValue("password2", "passwordInCorrect", "2개의 패스워드가 일치하지 않습니다.");
			return "user_signup_form";
		}

		try {
			userService.create(userCreateForm.getUsername(), userCreateForm.getEmail(), userCreateForm.getRole(),
					userCreateForm.getPassword1(), userCreateForm.getFirstName(), userCreateForm.getLastName());
		} catch (DataIntegrityViolationException e) {
			e.printStackTrace();
			bindingResult.reject("signupFailed", "이미 등록된 사용자입니다.");
			return "user_signup_form";
		} catch (Exception e) {
			e.printStackTrace();
			bindingResult.reject("signupFailed", e.getMessage());
			return "user_signup_form";
		}

		return "signupSuccess";
	}

	
	
	
    // Just one login page (all types of users login through this page)
    @GetMapping("/login")
    public String login() {
        return "user_login_form";
    }
    
//    @PostMapping("/login")
//    public String processLogin(@RequestParam("username") String username, @RequestParam("password") String password, Model model) {
//        
//   
//    	
//    	
//    	try {
////            // Create authentication token
////            UsernamePasswordAuthenticationToken authToken = new UsernamePasswordAuthenticationToken(username, password);
////            // Perform authentication
////            Authentication authentication = authenticationManager.authenticate(authToken);
////            // Set authentication in SecurityContext
////            SecurityContextHolder.getContext().setAuthentication(authentication);
////            // Redirect after successful login
//    	     // 현재 사용자의 인증 정보 가져오기
//            Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
//            
//            // 사용자명 가져오기
//            String username = authentication.getName();
//            
//            // CustomUserDetailsService를 통해 사용자 정보 가져오기
//            CustomUserDetails userDetails = customUserDetailsService.loadUserByUsername(username);
//            
//            // 사용자 정보를 모델에 추가
//            model.addAttribute("userDetails", userDetails);
//            return "redirect:/";
//            
//        } catch (UsernameNotFoundException e) {
//            // Handle case where username doesn't exist
//            model.addAttribute("errorMessage", "The provided username doesn't exist");
//            return "user_login_form";
//            
//        } catch (BadCredentialsException e) {
//            // Handle case where password is incorrect
//            model.addAttribute("errorMessage", "Incorrect password");
//            return "user_login_form";
//        }
//    }
}
