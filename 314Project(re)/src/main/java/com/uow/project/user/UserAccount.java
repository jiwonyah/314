package com.uow.project.user;

import java.util.List;

import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;

import lombok.Getter;

@Getter 
public class UserAccount extends User {
  private SiteUser user;
  public UserAccount(SiteUser user) {
    	super(user.getUsername(), user.getPassword(), List.of(new SimpleGrantedAuthority("ROLE_USER"))); 
        this.user = user; 
  } 
}
