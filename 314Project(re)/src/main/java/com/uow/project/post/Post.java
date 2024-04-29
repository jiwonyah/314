package com.uow.project.post;

import java.awt.Image;
import java.time.LocalDateTime;
import java.util.List;

//import com.example.demo.review.RentReview;

import jakarta.persistence.CascadeType;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
//import jakarta.persistence.Lob;
import jakarta.persistence.OneToMany;
import lombok.Getter;
import lombok.Setter;
import jakarta.persistence.ManyToOne;

import com.uow.project.post.field.Category;
import com.uow.project.post.field.FloorLevel;
import com.uow.project.post.field.Furnishing;
import com.uow.project.post.field.PropertyType;
import com.uow.project.user.SiteUser;

@Getter
@Setter
@Entity
public class Post {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "post_id")
    private Integer id;

    @Column(length = 200)
    private String subject;
 

    @Column(columnDefinition = "TEXT")
    private String content;
    
    @Enumerated(EnumType.STRING)
    private Category category;
    
    @Column(columnDefinition = "TEXT")
    private String address;
    
    @Enumerated(EnumType.STRING)
    private PropertyType propertyType;
    
    private int floorsize;
    
    @Enumerated(EnumType.STRING)
    private Furnishing furnishing;
    
    @Enumerated(EnumType.STRING)
    private FloorLevel floorlevel;
    
    private int top;
    
    private LocalDateTime createDate;

    //for rent
    @Column
    private int monthlyPrice;
    
    //for buy
    @Column
    private int price;
    
    @ManyToOne
    private SiteUser author;
    
    private LocalDateTime modifyDate;
    
	private int likeCount;

    private int viewCount;
    
//    @OneToMany(mappedBy = "board",fetch = FetchType.LAZY, cascade = CascadeType.PERSIST, orphanRemoval = true)
//    private List<Image> images;
    
    private boolean reportedStatus;
    
    public void increaseViewCount(){
        this.viewCount +=1;
    }
    

}

