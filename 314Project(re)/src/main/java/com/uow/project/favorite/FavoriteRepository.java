package com.uow.project.favorite;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.uow.project.post.Post;
import com.uow.project.user.SiteUser;

import java.util.List;
import java.util.Optional;
import java.util.Set;

@Repository
public interface FavoriteRepository extends JpaRepository<Favorite, Long> {

    // 특정 사용자의 특정 게시물 북마크 조회
    Optional<Favorite> findByUserAndPost(SiteUser user, Post post);
    
    /** member_id, lecture_id에 해당하는 wish 엔티티 존재 여부 반환 - 유저가 특정 강의를 찜 목록에 추가했는지 확인 **/
    boolean existsByUserIdAndPostId(Long userId, Integer postId);

    /** member_id, lecture_id에 해당하는 찜 엔티티 삭제 - 유저가 특정 강의 삭제 **/
    void deleteByUserIdAndPostId(Long userId, Integer postId);

}
