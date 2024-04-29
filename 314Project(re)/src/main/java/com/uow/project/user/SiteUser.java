package com.uow.project.user;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

import org.hibernate.Hibernate;

import com.uow.project.favorite.Favorite;
import com.uow.project.post.Post;

import jakarta.persistence.*;
import lombok.*;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Objects;
import java.util.Set;
@Getter
@Setter
@Entity
public class SiteUser{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "user_id")
    private Long id;

    @Column(nullable = false, unique = true, length = 30)
    private String username;

    @Column(nullable = false)
    private String password;
    
    @Column(unique = true)  
    private String email;
    
    @Column(nullable=false)
    @Enumerated(EnumType.STRING)
    private Role role;
    
    private String firstName;
    
    private String lastName;

    private double rating = 0;
    
    
    @OneToMany(mappedBy = "author", cascade = CascadeType.ALL)
    private List<Post> rents = new ArrayList<>();
    
    
    @Embedded
    private Profile profile;

    @Embeddable
    @NoArgsConstructor(access = AccessLevel.PROTECTED) @AllArgsConstructor(access = AccessLevel.PROTECTED)
    @Builder @Getter @ToString
    public static class Profile {
        private String location = null;
        @Lob @Basic(fetch = FetchType.EAGER)
        private String image = null;
    }
    
    
    @OneToMany(mappedBy = "user")
    private Set<Favorite> favorite = new HashSet<>();

    
//    public SiteUser(String username, String password) {
//        this.username = username;
//        this.password = password;
//    }

    @PrePersist
    protected void onCreate() {
        if (this.role == Role.BUYER || this.role == Role.SELLER) {
            this.firstName = null;
            this.lastName = null;
        }
        
        if (this.role == Role.ADMIN) {
            this.email = null;
            this.firstName = null;
            this.lastName = null;
        }

    }   
}