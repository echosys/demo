package com.onlinebanking.dao;
import com.onlinebanking.domain.ConfirmationToken;

import org.springframework.data.repository.CrudRepository;

import com.onlinebanking.domain.ConfirmationToken;

public interface ConfirmationTokenDAO extends CrudRepository<ConfirmationToken, String> {
    ConfirmationToken findByConfirmationToken(String confirmationToken);

}
