package com.project.app.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.project.app.entity.*;

public interface UserRepositoryAdmin extends JpaRepository<User, Long>{

}
