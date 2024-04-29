package com.uow.project.post.crud;

import java.security.Principal;

import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import com.uow.project.post.BuyForm;
import com.uow.project.post.PostRepository;
import com.uow.project.post.PostService;
import com.uow.project.post.RentForm;
import com.uow.project.user.SiteUser;
import com.uow.project.user.UserService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;


@RequiredArgsConstructor
@Controller
public class CreatePostController {
	
	private final PostService postService;
	private final UserService userService;
	private final PostRepository postRepository;
	
    //creating page for rent category
    //@PreAuthorize("hasAnyAuthority('ADMIN', 'AGENT','SELLER')")  이건 없어도 돼서 주석처리
    @GetMapping("/rent/create")
    public String rentCreate(RentForm rentForm) {
        if (!SecurityContextHolder.getContext().getAuthentication().getAuthorities().stream()
                .anyMatch(auth -> auth.getAuthority().equals("ADMIN") ||
                                  auth.getAuthority().equals("AGENT") ||
                                  auth.getAuthority().equals("SELLER"))) {
            // 특정 권한이 없는 경우 다른 페이지로 리다이렉트
            return "post/cannotPost"; 
        }
        return "post/rent_form";
    }
    
    @PreAuthorize("hasAnyAuthority('ADMIN', 'AGENT','SELLER')")
	@PostMapping("/rent/create")
	public String rentCreate(@Valid RentForm rentForm, BindingResult bindingResult, Principal principal) {
		if (bindingResult.hasErrors()) {
			return "post/rent_form";
		}
		SiteUser siteuser = this.userService.getUser(principal.getName());
		this.postService.createRent(rentForm.getSubject(), rentForm.getContent(), rentForm.getAddress(), rentForm.getPropertyType(),
				rentForm.getFloorsize(), rentForm.getFurnishing(), rentForm.getFloorlevel(), rentForm.getTop(), rentForm.getMonthlyPrice(),
				siteuser);
		return "redirect:/rent";
	}
    
    //------------------------------------buy-----------------------------------------
    
    //creating page for buy category
    @GetMapping("/buy/create")
    public String buyCreate(BuyForm buyForm) {
        if (!SecurityContextHolder.getContext().getAuthentication().getAuthorities().stream()
                .anyMatch(auth -> auth.getAuthority().equals("ADMIN") ||
                                  auth.getAuthority().equals("AGENT") ||
                                  auth.getAuthority().equals("SELLER"))) {
            // 특정 권한이 없는 경우 다른 페이지로 리다이렉트
            return "post/cannotPost"; 
        }
        return "post/buy_form";
    }
    
    @PreAuthorize("hasAnyAuthority('ADMIN', 'AGENT','SELLER')")
	@PostMapping("/buy/create")
	public String buyCreate(@Valid BuyForm buyForm, BindingResult bindingResult, Principal principal) {
		if (bindingResult.hasErrors()) {
			return "post/buy_form";
		}
		SiteUser siteuser = this.userService.getUser(principal.getName());
		this.postService.createBuy(buyForm.getSubject(), buyForm.getContent(), buyForm.getAddress(), buyForm.getPropertyType(),
				buyForm.getFloorsize(), buyForm.getFurnishing(), buyForm.getFloorlevel(), buyForm.getTop(), buyForm.getPrice(),
				siteuser);
		return "redirect:/buy";
	}
    
    
    
}
