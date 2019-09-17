package com.onlinebanking.dao;

import com.onlinebanking.domain.PrimaryAccount;
import org.springframework.data.repository.CrudRepository;
import com.onlinebanking.domain.CreditAccount;


/**
 * Created by z00382545 on 10/21/16.
 */
public interface CreditAccountDao extends CrudRepository<CreditAccount,Long> {

    CreditAccount findByAccountNumber (int accountNumber);
}
