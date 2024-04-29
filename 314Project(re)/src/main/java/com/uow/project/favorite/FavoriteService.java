package com.uow.project.favorite;

import java.util.Optional;
import java.util.Set;
import org.springframework.stereotype.Service;

import com.uow.project.DataNotFoundException;
import com.uow.project.post.Post;
import com.uow.project.post.PostRepository;
import com.uow.project.user.SiteUser;
import com.uow.project.user.UserRepository;

import lombok.RequiredArgsConstructor;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.transaction.annotation.Transactional;

@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)
public class FavoriteService {

    private final FavoriteRepository favoriteRepository;
    private final UserRepository userRepository;
    private final PostRepository postRepository;

    public boolean toggleFavorite(SiteUser user, Post post) {
        Optional<Favorite> existingFavorite = favoriteRepository.findByUserAndPost(user, post);

        if (existingFavorite.isPresent()) {
            // 만약 이미 즐겨찾기가 존재한다면, 해당 즐겨찾기를 삭제하여 즐겨찾기를 해제합니다.
            favoriteRepository.delete(existingFavorite.get());
            return false; // 즐겨찾기 해제됨
        } else {
            // 만약 즐겨찾기가 존재하지 않는다면, 새로운 즐겨찾기를 생성하여 추가합니다.
            Favorite newFavorite = new Favorite(user, post);
            favoriteRepository.save(newFavorite);
            return true; // 즐겨찾기 추가됨
        }
    }
  
}

