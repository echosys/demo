package com.onlinebanking.service;

import com.onlinebanking.dao.UserDao;
import com.onlinebanking.domain.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;

import java.util.List;

public interface EmployeeService {
    public List<User> getAllUsers();

    public void saveOrUpdate(User user);

    public Page<User> getPaginated(Pageable pageable);

}