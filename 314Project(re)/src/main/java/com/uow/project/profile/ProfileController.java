package com.uow.project.profile;

import java.security.Principal;
import java.util.Optional;

import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.uow.project.user.UserService;
//import com.uow.project.user.CurrentUser;
import com.uow.project.user.SiteUser;
import com.uow.project.user.UserRepository;

import lombok.RequiredArgsConstructor;

@Controller
@RequiredArgsConstructor
public class ProfileController {
    private final UserService userService;
    private final AuthenticationManager authenticationManager;
    private final UserRepository userRepository;

    @GetMapping("/profile/{username}")
    public String profile(@PathVariable("username") String username, Model model, @AuthenticationPrincipal SiteUser currentUser) {
        SiteUser user = userService.getUser(username);
        model.addAttribute("user", user);
        model.addAttribute("currentUser", currentUser);
        return "profile";
    }

    @GetMapping("/profile/{username}/edit")
    public String editProfile(@PathVariable("username") String username, Model model, @AuthenticationPrincipal SiteUser currentUser) {
        SiteUser user = userService.getUser(username);
        model.addAttribute("user", user);
        model.addAttribute("currentUser", currentUser);
        return "profile-edit";
    }

    @PostMapping("/profile/{username}/edit")
    public String updateProfile(@PathVariable("username") String username, @ModelAttribute SiteUser user, @AuthenticationPrincipal SiteUser currentUser, RedirectAttributes redirectAttributes) {
        currentUser.setFirstName(user.getFirstName());
        currentUser.setLastName(user.getLastName());
        currentUser.setEmail(user.getEmail());
        userService.update(currentUser);

        // 사용자 정보 업데이트 후 로그인 세션 갱신
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(currentUser.getUsername(), currentUser.getPassword()));
        SecurityContextHolder.getContext().setAuthentication(authentication);

        redirectAttributes.addFlashAttribute("message", "Profile updated.");
        return "redirect:/profile/{username}";
    }
}



