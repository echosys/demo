package com.onlinebanking.dao;
import com.onlinebanking.domain.UserAccountRequest;
import java.util.List;
import org.springframework.data.repository.CrudRepository;

public interface UserAccountRequestDao extends CrudRepository<UserAccountRequest, Long> {
    UserAccountRequest findByUsername(String username);
    UserAccountRequest findByPhone(String phone);
    List<UserAccountRequest> findAll();
    List<UserAccountRequest> findByEnabled(Boolean enabled);
}