package com.Project.repository;

import org.springframework.data.jpa.repository.JpaRepository;

import com.Project.entity.UserAccount;

public interface UserRepository extends JpaRepository<UserAccount, Long> {
	
	UserAccount findByUsername(String username);
}
