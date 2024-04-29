package com.uow.project.post;

import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;
import com.uow.project.DataNotFoundException;
import com.uow.project.post.field.Category;
import com.uow.project.post.field.FloorLevel;
import com.uow.project.post.field.Furnishing;
import com.uow.project.post.field.PropertyType;
import com.uow.project.user.SiteUser;
import com.uow.project.user.UserRepository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import jakarta.persistence.criteria.Join;
import jakarta.persistence.criteria.JoinType;
import jakarta.persistence.criteria.Predicate;
import jakarta.persistence.criteria.Root;
import org.springframework.data.jpa.domain.Specification;

@RequiredArgsConstructor
@Service
public class PostService {
    private final PostRepository postRepository;
    private final UserRepository userRepository;
    
	public Page<Post> getList(int page, String kw) {
		List<Sort.Order> sorts = new ArrayList<>();
		sorts.add(Sort.Order.desc("createDate"));
		Pageable pageable = PageRequest.of(page, 10, Sort.by(sorts));
		Specification<Post> spec = search(kw);
		return this.postRepository.findAll(spec, pageable);
	}
	
	public Page<Post> getPostsByCategory(Category category, int page, String kw) {
	    Pageable pageable = PageRequest.of(page, 10, Sort.by(Sort.Direction.DESC, "createDate"));
	    return postRepository.findByCategory(category, pageable);
	}
    
    public Post getPost(Integer id) {  
        Optional<Post> rent = this.postRepository.findById(id);
        if (rent.isPresent()) {
            return rent.get();
        } else {
            throw new DataNotFoundException("The rent post not found");
        }
    }
    
    public Post getPost(Integer id, Category category) {
        Optional<Post> post = null;

        switch (category) {
            case RENT:
                post = this.postRepository.findById(id);
                break;
            case BUY:
                post = this.postRepository.findById(id);
                break;
            // 다른 카테고리에 대한 처리 추가
            default:
                throw new IllegalArgumentException("Unsupported category");
        }

        if (post.isPresent()) {
            return post.get();
        } else {
            throw new DataNotFoundException("The post not found");
        }
    }
    
    
    //------------------------Rent-----------------------------

    public void createRent(String subject, String content,
    		String address, PropertyType propertyType,
    		int floorsize, Furnishing furnishing,
    		FloorLevel floorlevel, 
    		int top, int monthlyPrice, SiteUser user) {
        Post p = new Post();
        p.setSubject(subject);
        p.setContent(content);
        p.setAddress(address);
        p.setPropertyType(propertyType);
        p.setFloorsize(floorsize);
        p.setFurnishing(furnishing);
        p.setFloorlevel(floorlevel);
        p.setTop(top);
        p.setMonthlyPrice(monthlyPrice);
        p.setAuthor(user);
        p.setCategory(Category.RENT);
        p.setCreateDate(LocalDateTime.now());
        this.postRepository.save(p);
    }
    
    public void modifyRent(Post rent, String subject, String content,
    		String address, PropertyType propertyType,
    		int floorsize, Furnishing furnishing,
    		FloorLevel floorlevel, 
    		int top, int monthlyPrice) {
    	rent.setSubject(subject);
    	rent.setContent(content);
    	rent.setAddress(address);
    	rent.setPropertyType(propertyType);
    	rent.setFloorsize(floorsize);
    	rent.setFurnishing(furnishing);
    	rent.setFloorlevel(floorlevel);
    	rent.setTop(top);
    	rent.setMonthlyPrice(monthlyPrice);
    	rent.setModifyDate(LocalDateTime.now());
        this.postRepository.save(rent);
    }
    
    
    //-----------------------Buy----------------------------
    public void createBuy(String subject, String content,
    		String address, PropertyType propertyType,
    		int floorsize, Furnishing furnishing,
    		FloorLevel floorlevel, 
    		int top, int price, SiteUser user) {
        Post p = new Post();
        p.setSubject(subject);
        p.setContent(content);
        p.setAddress(address);
        p.setPropertyType(propertyType);
        p.setFloorsize(floorsize);
        p.setFurnishing(furnishing);
        p.setFloorlevel(floorlevel);
        p.setTop(top);
        p.setPrice(price);
        p.setAuthor(user);
        p.setCategory(Category.BUY);
        p.setCreateDate(LocalDateTime.now());
        this.postRepository.save(p);
    }
    
    public void modifyBuy(Post buy, String subject, String content,
    		String address, PropertyType propertyType,
    		int floorsize, Furnishing furnishing,
    		FloorLevel floorlevel, 
    		int top, int price) {
    	buy.setSubject(subject);
    	buy.setContent(content);
    	buy.setAddress(address);
    	buy.setPropertyType(propertyType);
    	buy.setFloorsize(floorsize);
    	buy.setFurnishing(furnishing);
    	buy.setFloorlevel(floorlevel);
    	buy.setTop(top);
    	buy.setPrice(price);
    	buy.setModifyDate(LocalDateTime.now());
        this.postRepository.save(buy);
    }
    
    
    
    
    public void delete(Post post) {
        this.postRepository.delete(post);
    }
    
    
    
    private Specification<Post> search(String kw) {
        return new Specification<>() {
            private static final long serialVersionUID = 1L;
            @Override
            public Predicate toPredicate(Root<Post> r, CriteriaQuery<?> query, CriteriaBuilder cb) {
                query.distinct(true);  // 중복을 제거 
                Join<Post, SiteUser> u1 = r.join("author", JoinType.LEFT);

                return cb.or(cb.like(r.get("subject"), "%" + kw + "%"),    
                   
                        cb.like(u1.get("username"), "%" + kw + "%"));    // post author 
            }
        };
    }
    
    
}
