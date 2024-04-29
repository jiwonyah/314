package com.uow.project.user;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;

import lombok.Data;
import lombok.Getter;


//사용자 정보를 UserDetails 인터페이스로 구현.
@Data
@Getter
public class CustomUserDetails implements UserDetails {
    private SiteUser user;

    /* 일반 로그인 생성자 */
    public CustomUserDetails(SiteUser user) {
        this.user = user;
    }

    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        List<SimpleGrantedAuthority> authorities = new ArrayList<>();
         
        authorities.add(new SimpleGrantedAuthority(user.getRole().toString()));
         
        return authorities;
    }
    
    
    //----------------------------------------------------------------UserDetails

    @Override
    public String getPassword() {
        return user.getPassword();
    }

    @Override
    public String getUsername() {
        return user.getUsername();
    }

    @Override
    public boolean isAccountNonExpired() {
        return true;
    }

    @Override
    public boolean isAccountNonLocked() {
        return true;
    }

    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }

    @Override
    public boolean isEnabled() {
        return true;
    }

}
