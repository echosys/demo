package com.onlinebanking.service.UserServiceImpl;

import java.util.List;
import java.util.Set;

import org.hibernate.usertype.UserType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.onlinebanking.dao.RoleDao;
import com.onlinebanking.dao.UserAccountRequestDao;
import com.onlinebanking.domain.UserAccountRequest;
import com.onlinebanking.domain.security.UserRole;
import com.onlinebanking.service.AccountService;
import com.onlinebanking.service.UserAccountRequestService;
import com.onlinebanking.enums.*;

@Service
@Transactional
public class UserAccountRequestImpl implements UserAccountRequestService{

    private static final Logger LOG = LoggerFactory.getLogger(UserAccountRequestService.class);

    @Autowired
    private UserAccountRequestDao userAccountRequestDao;

    @Autowired
    private RoleDao roleDao;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    @Autowired
    private AccountService accountService;

    public void save(UserAccountRequest request) {
        userAccountRequestDao.save(request);
    }

    public UserAccountRequest findByUsername(String username) {
        return userAccountRequestDao.findByUsername(username);
    }



    public UserAccountRequest findByPhone(String phone) {
        return userAccountRequestDao.findByPhone(phone);
    }


    public UserAccountRequest createRequest(UserAccountRequest request) {
        //User localUser = userDao.findByUsername(user.getUsername());

//        if (localUser != null) {
//            LOG.info("User with username {} already exist. Nothing will be done. ", user.getUsername());
//        } else {
//            String encryptedPassword = passwordEncoder.encode(user.getPassword());
//            user.setPassword(encryptedPassword);
//
//            for (UserRole ur : userRoles) {
//                roleDao.save(ur.getRole());
//            }
//
//            user.getUserRoles().addAll(userRoles);
//            user.setPrimaryAccount(accountService.createPrimaryAccount());
//            user.setSavingsAccount(accountService.createSavingsAccount());
//
//            localUser = userDao.save(user);
//        }

        String encryptedPassword = passwordEncoder.encode(request.getPassword());
        request.setPassword(encryptedPassword);
        UserAccountRequest r=userAccountRequestDao.save(request);
        System.out.println("-------------------------------------------");
        System.out.println(request);
        return r;
    }

    public boolean checkUserExists(String username){
        if (checkUsernameExists(username)) {
            return true;
        } else {
            return false;
        }
    }

    public boolean checkUsernameExists(String username) {
        if (null != findByUsername(username)) {
            return true;
        }

        return false;
    }


    public UserAccountRequest saveRequest (UserAccountRequest request) {
        return userAccountRequestDao.save(request);
    }

    public List<UserAccountRequest> findUserAccountRequestList() {
        return userAccountRequestDao.findAll();
    }

    public void enableUserAccountRequest (String username) {
        UserAccountRequest request = findByUsername(username);
        request.setEnabled(true);
        userAccountRequestDao.save(request);
    }

    public void disableUserAccountRequest (String username) {
        UserAccountRequest user = findByUsername(username);
        user.setEnabled(false);
        System.out.println(user.isEnabled());
        userAccountRequestDao.save(user);
        System.out.println(username + " is disabled.");
    }
}
