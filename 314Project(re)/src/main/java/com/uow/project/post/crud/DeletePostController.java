package com.uow.project.post.crud;

import java.security.Principal;

import org.springframework.http.HttpStatus;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.server.ResponseStatusException;

import com.uow.project.post.Post;
import com.uow.project.post.PostRepository;
import com.uow.project.post.PostService;
import com.uow.project.post.field.Category;
import com.uow.project.user.UserService;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Controller
public class DeletePostController {
	private final PostService postService;
	private final UserService userService;
	private final PostRepository postRepository;
	
    @PreAuthorize("isAuthenticated()")
    @GetMapping("/rent/delete/{id}")
    public String rentDelete(Principal principal, @PathVariable("id") Integer id) {
        Post rent = this.postService.getPost(id, Category.RENT);
        if (!rent.getAuthor().getUsername().equals(principal.getName())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "You don't have authority to remove the post.");
        }
        this.postService.delete(rent);
        return "redirect:/rent";
    }
    
    @PreAuthorize("isAuthenticated()")
    @GetMapping("/buy/delete/{id}")
    public String buyDelete(Principal principal, @PathVariable("id") Integer id) {
        Post buy = this.postService.getPost(id, Category.BUY);
        if (!buy.getAuthor().getUsername().equals(principal.getName())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "You don't have authority to remove the post.");
        }
        this.postService.delete(buy);
        return "redirect:/buy";
    }
    
}
