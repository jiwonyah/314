package com.example.demo.user;

import lombok.Getter;

@Getter
public enum Role {
    ADMIN("ROLE_ADMIN"),
    USER("ROLE_USER"),
    AGENT("ROLE_AGENT");
	
    Role(String value) {
        this.value = value;
    }

    private String value;    
    
}
