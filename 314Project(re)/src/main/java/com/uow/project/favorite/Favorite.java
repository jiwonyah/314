package com.uow.project.favorite;

import com.uow.project.post.Post;
import com.uow.project.user.SiteUser;

import jakarta.persistence.*;
import lombok.Getter;
import lombok.Setter;

@Entity
@Getter
@Setter
public class Favorite {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    private SiteUser user;

    @ManyToOne
    private Post post;

    // 생성자, 유저와 게시물 연결
    public Favorite(SiteUser user, Post post) {
        this.user = user;
        this.post = post;
    }

    // getter, setter
    // ...
}
