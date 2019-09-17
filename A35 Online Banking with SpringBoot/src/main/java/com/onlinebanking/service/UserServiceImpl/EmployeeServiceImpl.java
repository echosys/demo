package com.onlinebanking.service.UserServiceImpl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import com.onlinebanking.service.EmployeeService;
import java.util.List;

import com.onlinebanking.domain.User;
import com.onlinebanking.dao.EmployeeDao;
@Service
public class EmployeeServiceImpl implements EmployeeService {
    @Autowired
    private EmployeeDao employeeDao;


    @Override
    public List<User> getAllUsers()
    {
        return (List<User>) employeeDao.findAll();
    }

    @Override
    public void saveOrUpdate(User user) {
        employeeDao.save(user);
    }

    @Override
    public Page<User> getPaginated(Pageable pageable) {
        return employeeDao.findAll(pageable);
    }

}