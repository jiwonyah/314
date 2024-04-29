package com.uow.project.user;

import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.*;
import org.springframework.stereotype.Service;
 
@Service
public class CustomUserDetailsService implements UserDetailsService {
    @Autowired private UserRepository userRepository;
 
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
    	//유저가 db에 있는지 검색
    	//username으로 검색할거임 (unique)
    	Optional<SiteUser> _siteUser = this.userRepository.findByusername(username);
        if (_siteUser == null) {
            throw new UsernameNotFoundException("No user is found with the given username.");
        }
        SiteUser siteUser = _siteUser.get();
        
        //UserDetailsService 객체 반환
        return new CustomUserDetails(siteUser);
    }
}
