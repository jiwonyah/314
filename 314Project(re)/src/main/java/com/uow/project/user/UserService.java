package com.uow.project.user;


import lombok.RequiredArgsConstructor;

import java.util.Optional;

import org.springframework.stereotype.Service;

import com.uow.project.DataNotFoundException;

import org.springframework.security.crypto.password.PasswordEncoder;

@Service
@RequiredArgsConstructor
public class UserService{
	private final UserRepository userRepository;
	private final PasswordEncoder passwordEncoder;

    public SiteUser create(String username, String email, Role role ,String password, String firstName,
    		String lastName) {
    	SiteUser user = new SiteUser();
        user.setUsername(username);
        user.setEmail(email);
        user.setRole(role);
        user.setPassword(passwordEncoder.encode(password));
        user.setFirstName(firstName);
        user.setLastName(lastName);
        this.userRepository.save(user);
        return user;
    }

	public SiteUser getUser(String username) {
		Optional<SiteUser> siteUser = this.userRepository.findByusername(username);
		if (siteUser.isPresent()) {
			return siteUser.get();
		} else {
			throw new DataNotFoundException("siteuser not found");
		}
	}
	
    public SiteUser update(SiteUser user) {
        return userRepository.save(user);
    }
}