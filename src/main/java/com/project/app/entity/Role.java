package com.project.app.entity;


import lombok.Getter;

@Getter
public enum Role {

	 ADMIN("ADMIN"),
	 USER("USER"),
	 SELLER("SELLER"),
	 AGENT("AGENT");
	
		
	 Role(String value) {
		 this.value = value;
	 }

	 private String value;  
}
