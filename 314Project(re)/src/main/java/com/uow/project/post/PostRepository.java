package com.uow.project.post;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.uow.project.post.field.Category;

import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.domain.Specification;


public interface PostRepository extends JpaRepository<Post, Integer> {
	Post findBySubject(String subject);

	Post findBySubjectAndContent(String subject, String content);

	List<Post> findBySubjectLike(String subject);

	Page<Post> findAll(Pageable pageable);
	
	Page<Post> findAll(Specification<Post> spec, Pageable pageable);
	
	Page<Post> findByCategory(Category category, Pageable pageable);
}