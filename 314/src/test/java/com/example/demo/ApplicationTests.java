package com.example.demo;
import com.example.demo.user.UserRepository;
import com.example.demo.user.SiteUser;
import com.example.demo.user.Role;
//import java.time.LocalDateTime;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class ApplicationTests {
    @Autowired
    private UserRepository userRepository;

    @Test
    void testJpa() {        
        SiteUser user1 = new SiteUser();
        user1.setId(1L);
        user1.setUsername("abcd");
        user1.setPassword("1234");
        user1.setRole(Role.USER);
        this.userRepository.save(user1);  // 첫번째 질문 저장

    }

}
