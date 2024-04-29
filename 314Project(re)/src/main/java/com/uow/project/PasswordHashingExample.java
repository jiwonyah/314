package com.uow.project;

import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;


//this class is to create hashed version of password (when creating admin)
public class PasswordHashingExample {
    public static void main(String[] args) {
        // enter any password you want
        String password = "sa1234";

        BCryptPasswordEncoder encoder = new BCryptPasswordEncoder();

        String hashedPassword = encoder.encode(password);

        System.out.println("Hashed Password: " + hashedPassword);
    }
}