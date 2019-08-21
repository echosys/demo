package com.onlinebanking.service.UserServiceImpl;

import com.onlinebanking.enums.UserTypes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import com.onlinebanking.service.AdminService;

import java.util.Iterator;
import java.util.List;
import java.security.Principal;
import com.onlinebanking.domain.User;
import com.onlinebanking.dao.AdminDao;
import java.util.stream.Collectors;

@Service
public class AdminServiceImpl implements AdminService {



    @Autowired
    private AdminDao adminDao;

    @Override
    public List<User> getAllUsers()
    {
        return (List<User>) adminDao.findAll();
    }

   // @Override
    //public User getUserbyID(Long helpid) {
      //  return adminDao.findById(helpid).get();
    //}

    @Override
    public void saveOrUpdate(User user) {
        adminDao.save(user);
    }

    // @Override
    // public void deleteHelp(Long helpid) {
    //     adminDao.deleteById(helpid);
    // }


    @Override
    public Page<User> getPaginated(Pageable pageable) {
        Page<User> users = adminDao.findAll(pageable);
        Iterator<User> it = users.iterator();
        while (it.hasNext()) {
                User user = (User) it.next();
                if(user.getUserTypeId() == UserTypes.ADMIN.getType()) {
                    it.remove();
                }
        }

        return users;
    }


    public void deleteEmployeeByName(String recipientName) {
        adminDao.deleteByUsername(recipientName);
    }
    
    public List<User> findEmployeeList(Principal principal) {
        String username = principal.getName();
        List<User> recipientList = adminDao.findAll().stream() 			//convert list to stream
                .filter(user -> username.equals(user.getUsername()))	//filters the line, equals to username
                .collect(Collectors.toList());

        return recipientList;
    }
}