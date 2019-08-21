package com.onlinebanking.dao;

import java.util.List;

import org.springframework.data.repository.CrudRepository;


import com.onlinebanking.domain.CreditTransaction;

public interface CreditTransactionDao extends CrudRepository<CreditTransaction, Long> {

    List<CreditTransaction> findAll();
}
