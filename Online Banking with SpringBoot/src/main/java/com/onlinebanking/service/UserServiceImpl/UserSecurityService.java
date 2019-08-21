package com.onlinebanking.service.UserServiceImpl;

import com.onlinebanking.domain.security.UserRole;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.onlinebanking.dao.UserDao;
import com.onlinebanking.domain.User;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

@Service
public class UserSecurityService implements UserDetailsService {

    /** The application logger */
    private static final Logger LOG = LoggerFactory.getLogger(UserSecurityService.class);

    @Autowired
    private UserDao userDao;

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User user = userDao.findByUsername(username);
        if (null == user) {
            LOG.warn("Username {} not found", username);
            throw new UsernameNotFoundException("Username " + username + " not found");
        }
        Set<UserRole> userRoles = user.getUserRoles();

        List<GrantedAuthority> authorities = new ArrayList<GrantedAuthority>();

        for(UserRole role:userRoles){
            authorities.add(new SimpleGrantedAuthority(role.getRole().getName()));
        }

        UserDetails userDetails = (UserDetails) new org.springframework.security.core.userdetails.User(user.getUsername(),
                user.getPassword(), authorities);

        return userDetails;
    }
}
