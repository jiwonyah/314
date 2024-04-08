package com.example.demo.user;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UserCreateForm {
    @Size(min = 3, max = 25)
    @NotEmpty(message = "UserId is mandatory.")
    private String username;

    @NotEmpty(message = "Password is mandatory.")
    private String password1;

    @NotEmpty(message = "Check the password.")
    private String password2;
    
    @NotEmpty(message = "Email is mandatory.")
    @Email
    private String email;

}
