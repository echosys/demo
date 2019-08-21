package com.onlinebanking.service;


import com.onlinebanking.dao.UserDao;
import com.onlinebanking.domain.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import java.security.Principal;
import java.util.List;

public interface AdminService {
    public List<User> getAllUsers();

    // public User getCheckByID(Long helpid);

    public void saveOrUpdate(User user);

    // public void deleteHelp(Long id);

    public Page<User> getPaginated(Pageable pageable);
    
    void deleteEmployeeByName(String recipientName);

    List<User> findEmployeeList(Principal principal);
}