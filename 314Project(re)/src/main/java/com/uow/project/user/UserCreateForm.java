package com.uow.project.user;

import jakarta.persistence.PrePersist;

//import org.hibernate.validator.constraints.Length;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class UserCreateForm {
    @Size(min = 3, max = 20) 
    @Pattern(regexp = "^[a-zA-Z0-9]{3,20}$") 
    private String username;

    @NotEmpty(message = "Password is mandatory.")
    @Size(min = 8, max = 50)
    private String password1;

    @NotEmpty(message = "Check the password.")
    @Size(min = 8, max = 50)
    private String password2;
    
    @NotEmpty(message = "Email is mandatory.")
    @Email
    private String email;
    
    @NotNull(message = "Select your role")
    private Role role;
    
    private String firstName;
    
    private String lastName;
    
    
    @PrePersist
    protected void onCreate() {
        if (this.role == Role.BUYER || this.role == Role.SELLER) {
            this.firstName = null;
            this.lastName = null;
        }
    }
    
}
