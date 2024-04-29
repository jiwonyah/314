package com.uow.project.user;


import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.transaction.annotation.Transactional;

public interface UserRepository extends JpaRepository<SiteUser, Long> {

	Optional<SiteUser> findByusername(String username);
}