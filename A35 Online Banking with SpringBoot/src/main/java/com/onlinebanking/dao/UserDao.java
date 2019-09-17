package com.onlinebanking.dao;

import java.util.List;

import org.springframework.data.repository.CrudRepository;

import com.onlinebanking.domain.User;

public interface UserDao extends CrudRepository<User, Long> {
	User findByUsername(String username);
    User findByEmail(String email);
    User findByPhone(String phone);
    List<User> findByUserTypeId(int usertypeid);
    List<User> findAll();
}
