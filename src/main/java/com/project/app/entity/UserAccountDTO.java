package com.project.app.entity;

import java.time.LocalDate;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UserAccountDTO {
	
	private String fullName;
	private LocalDate dob;
	private String email;
	private String username;
	private String password;

}
