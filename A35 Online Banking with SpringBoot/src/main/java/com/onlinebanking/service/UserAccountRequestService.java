package com.onlinebanking.service;

import java.util.List;
import java.util.Set;

import com.onlinebanking.domain.UserAccountRequest;

public interface UserAccountRequestService {
    UserAccountRequest findByUsername(String username);

    UserAccountRequest findByPhone(String phone);

    boolean checkUserExists(String username);

    boolean checkUsernameExists(String username);

    void save (UserAccountRequest request);

    UserAccountRequest createRequest(UserAccountRequest request);

    UserAccountRequest saveRequest (UserAccountRequest request);

    List<UserAccountRequest> findUserAccountRequestList();

    void enableUserAccountRequest (String username);

    void disableUserAccountRequest (String username);
}
