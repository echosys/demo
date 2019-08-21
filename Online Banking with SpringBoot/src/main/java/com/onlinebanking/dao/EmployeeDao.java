package com.onlinebanking.dao;

import org.springframework.data.repository.CrudRepository;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.onlinebanking.domain.PrimaryTransaction;
import com.onlinebanking.domain.User;
import com.onlinebanking.domain.security.UserRole;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.Query;

public interface EmployeeDao extends CrudRepository<User, Long> {
    Page<User> findAll(Pageable pageable);
}
