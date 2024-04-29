package com.uow.project.favorite;

import java.io.IOException;

import org.springframework.security.core.Authentication;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import com.uow.project.DataNotFoundException;
import com.uow.project.post.Post;
import com.uow.project.post.PostRepository;
import com.uow.project.post.PostService;
import com.uow.project.user.CustomUserDetails;
import com.uow.project.user.SiteUser;
import com.uow.project.user.UserService;

import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor
@Controller
public class FavoriteController {
	
	private final UserService userService;
	private final FavoriteService favoriteService;
	private final PostService postService;
	
	
	@ResponseBody
	@GetMapping("/rent/detail/{postId}/favorite")
	public boolean rentFavorite(@PathVariable("contentId") Integer postId, 
			@AuthenticationPrincipal CustomUserDetails userDetails) throws IOException{
		// 현재 사용자 정보를 통해 사용자 이름(username)을 가져옵니다.
		String username = userDetails.getUsername();
		// 사용자 이름을 이용하여 UserService의 getUser 메서드를 호출하여 SiteUser 객체를 가져옵니다.
		SiteUser user = userService.getUser(username);
	    Post post = postService.getPost(postId);
	    return favoriteService.toggleFavorite(user, post);
	}	
	
	
	@ResponseBody
	@GetMapping("/buy/detail/{postId}/favorite")
	public boolean buyFavorite(@PathVariable("contentId") Integer postId, 
			@AuthenticationPrincipal CustomUserDetails userDetails) throws IOException{
		// 현재 사용자 정보를 통해 사용자 이름(username)을 가져옵니다.
		String username = userDetails.getUsername();
		// 사용자 이름을 이용하여 UserService의 getUser 메서드를 호출하여 SiteUser 객체를 가져옵니다.
		SiteUser user = userService.getUser(username);
	    Post post = postService.getPost(postId);
	    return favoriteService.toggleFavorite(user, post);
	}	
}