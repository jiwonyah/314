package com.uow.project.post.crud;

import org.springframework.data.domain.Page;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;

import com.uow.project.post.Post;
import com.uow.project.post.PostRepository;
import com.uow.project.post.PostService;
import com.uow.project.post.field.Category;
import com.uow.project.user.UserService;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Controller
public class ReadPostController {
	
	private final PostService postService;
	private final UserService userService;
	private final PostRepository postRepository;
	
	//view list
    @GetMapping("/rent")
    public String post_rent(Model model, @RequestParam(value = "page", defaultValue = "0") int page,
    		@RequestParam(value = "kw", defaultValue = "") String kw) {
    	Page<Post> paging = this.postService.getPostsByCategory(Category.RENT, page, kw);
    	
        model.addAttribute("paging", paging);
        model.addAttribute("kw", kw);
        addAuthenticationAttributes(model);
        return "post/rent_list";
    }
    
    
    @GetMapping("/buy")
    public String post_buy(Model model, @RequestParam(value = "page", defaultValue = "0") int page,
    		@RequestParam(value = "kw", defaultValue = "") String kw) {
    	Page<Post> paging = this.postService.getPostsByCategory(Category.BUY, page, kw);
    	
        model.addAttribute("paging", paging);
        model.addAttribute("kw", kw);
        addAuthenticationAttributes(model);

        return "post/buy_list";
    }

    
    //view post detail
    @GetMapping(value = "/rent/detail/{id}")
    public String rent_detail(Model model, @PathVariable("id") Integer id) {
        Post rent = this.postService.getPost(id, Category.RENT);
        model.addAttribute("rent", rent);
    	
    	return "post/rent_detail";
    }

    
    @GetMapping(value = "/buy/detail/{id}")
    public String buy_detail(Model model, @PathVariable("id") Integer id) {
        Post buy = this.postService.getPost(id, Category.BUY);
        model.addAttribute("buy", buy);
    	
    	return "post/buy_detail";
    }
    
    private void addAuthenticationAttributes(Model model) {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication != null && authentication.isAuthenticated()) {
            String username = authentication.getName();
            model.addAttribute("username", username);

            boolean isAdmin = authentication.getAuthorities().stream()
                    .anyMatch(auth -> auth.getAuthority().equals("ADMIN"));
            boolean isAgent = authentication.getAuthorities().stream()
                    .anyMatch(auth -> auth.getAuthority().equals("AGENT"));
            boolean isSeller = authentication.getAuthorities().stream()
                    .anyMatch(auth -> auth.getAuthority().equals("SELLER"));
            boolean isBuyer = authentication.getAuthorities().stream()
                    .anyMatch(auth -> auth.getAuthority().equals("BUYER"));

            model.addAttribute("isAdmin", isAdmin);
            model.addAttribute("isAgent", isAgent);
            model.addAttribute("isSeller", isSeller);
            model.addAttribute("isBuyer", isBuyer);
        }
    }
}


