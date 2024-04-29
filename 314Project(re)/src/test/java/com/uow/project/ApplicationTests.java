package com.uow.project;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import com.uow.project.post.PostService;
import com.uow.project.post.field.FloorLevel;
import com.uow.project.post.field.Furnishing;
import com.uow.project.post.field.PropertyType;
import com.uow.project.user.SiteUser;

@SpringBootTest
class ApplicationTests {

    @Autowired
    private PostService postService;
	
	@Test
	void testJpa() {
		// creating sample posts
        for (int i = 1; i <= 30; i++) {
            String subject = String.format("Test Data:[%03d]", i);
            String content = "no contents";
            String address = "no contents";
            PropertyType propertyType = PropertyType.HDB;
            int floorsize = 50;
            Furnishing furnishing = Furnishing.PartiallyFurnished;
            FloorLevel floorlevel = FloorLevel.High;
            int top = 2000;
            int monthlyPrice = 3000;
                        
            this.postService.createRent(subject, content, address, propertyType, floorsize, furnishing,
            		floorlevel, top, monthlyPrice, null);
        }
  
        
        //login
        //create admin?
        //signup
        
        
	}

}
