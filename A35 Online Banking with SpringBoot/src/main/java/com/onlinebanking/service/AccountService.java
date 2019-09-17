package com.onlinebanking.service;

import java.security.Principal;

import com.onlinebanking.domain.PrimaryAccount;
import com.onlinebanking.domain.PrimaryTransaction;
import com.onlinebanking.domain.SavingsAccount;
import com.onlinebanking.domain.SavingsTransaction;
import com.onlinebanking.domain.CreditAccount;
import com.onlinebanking.domain.CreditTransaction;
import com.onlinebanking.domain.*;

public interface AccountService {
	PrimaryAccount createPrimaryAccount();
    SavingsAccount createSavingsAccount();
    CreditAccount createCreditAccount();
    void deposit(String accountType, double amount, Principal principal);
    void withdraw(User user, String accountType, double amount, Principal principal);
    
    
}
