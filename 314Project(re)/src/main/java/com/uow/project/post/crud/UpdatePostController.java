package com.uow.project.post.crud;

import java.security.Principal;

import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.server.ResponseStatusException;

import com.uow.project.post.BuyForm;
import com.uow.project.post.Post;
import com.uow.project.post.PostRepository;
import com.uow.project.post.PostService;
import com.uow.project.post.RentForm;
import com.uow.project.post.field.Category;
import com.uow.project.user.UserService;

import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Controller
public class UpdatePostController {
	private final PostService postService;
	private final UserService userService;
	private final PostRepository postRepository;
	
    //modification
    @PreAuthorize("hasAnyAuthority('ADMIN', 'AGENT','SELLER')")
    @GetMapping("/rent/modify/{id}")
    public String rentModify(RentForm rentForm, @PathVariable("id") Integer id, Principal principal) {
        Post rent = this.postService.getPost(id, Category.RENT);
        if(!rent.getAuthor().getUsername().equals(principal.getName())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "You don't have authority to modify the post");
        }
        rentForm.setSubject(rent.getSubject());
        rentForm.setContent(rent.getContent());
        rentForm.setAddress(rent.getAddress());
        rentForm.setPropertyType(rent.getPropertyType());
        rentForm.setFloorsize(rent.getFloorsize());
        rentForm.setFurnishing(rent.getFurnishing());
        rentForm.setFloorlevel(rent.getFloorlevel());
        rentForm.setTop(rent.getTop());
        rentForm.setMonthlyPrice(rent.getMonthlyPrice());
        return "post/rent_form";
    }
    
    @PreAuthorize("isAuthenticated()")
    @PostMapping("/rent/modify/{id}")
    public String rentModify(@Valid RentForm rentForm, BindingResult bindingResult, 
            Principal principal, @PathVariable("id") Integer id) {
        if (bindingResult.hasErrors()) {
            return "post/rent_form";
        }
        Post rent = this.postService.getPost(id, Category.RENT);
        if (!rent.getAuthor().getUsername().equals(principal.getName())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "You don't have authority to modify the post");
        }
        this.postService.modifyRent(rent, rentForm.getSubject(), rentForm.getContent(), rentForm.getAddress(), rentForm.getPropertyType(),
        		rentForm.getFloorsize(), rentForm.getFurnishing(), rentForm.getFloorlevel(), rentForm.getTop(), rentForm.getMonthlyPrice());
        return String.format("redirect:/rent/detail/%s", id);
    }
    
    //--------------------------------------buy-----------------------------------------
    
    //modification
    @PreAuthorize("hasAnyAuthority('ADMIN', 'AGENT','SELLER')")
    @GetMapping("/buy/modify/{id}")
    public String buyModify(BuyForm buyForm, @PathVariable("id") Integer id, Principal principal) {
        Post buy = this.postService.getPost(id, Category.BUY);
        if(!buy.getAuthor().getUsername().equals(principal.getName())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "You don't have authority to modify the post");
        }
        buyForm.setSubject(buy.getSubject());
        buyForm.setContent(buy.getContent());
        buyForm.setAddress(buy.getAddress());
        buyForm.setPropertyType(buy.getPropertyType());
        buyForm.setFloorsize(buy.getFloorsize());
        buyForm.setFurnishing(buy.getFurnishing());
        buyForm.setFloorlevel(buy.getFloorlevel());
        buyForm.setTop(buy.getTop());
        buyForm.setPrice(buy.getPrice());
        return "post/buy_form";
    }
    
    @PreAuthorize("isAuthenticated()")
    @PostMapping("/buy/modify/{id}")
    public String buyModify(@Valid BuyForm buyForm, BindingResult bindingResult, 
            Principal principal, @PathVariable("id") Integer id) {
        if (bindingResult.hasErrors()) {
            return "post/buy_form";
        }
        Post rent = this.postService.getPost(id, Category.BUY);
        if (!rent.getAuthor().getUsername().equals(principal.getName())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "You don't have authority to modify the post");
        }
        this.postService.modifyBuy(rent, buyForm.getSubject(), buyForm.getContent(), buyForm.getAddress(), buyForm.getPropertyType(),
        		buyForm.getFloorsize(), buyForm.getFurnishing(), buyForm.getFloorlevel(), buyForm.getTop(), buyForm.getPrice());
        return String.format("redirect:/buy/detail/%s", id);
    }
}
