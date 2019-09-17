package com.onlinebanking.service.UserServiceImpl;

import java.math.BigDecimal;
import java.security.Principal;
import java.util.Date;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.onlinebanking.dao.PrimaryAccountDao;
import com.onlinebanking.dao.SavingsAccountDao;
import com.onlinebanking.domain.PrimaryAccount;
import com.onlinebanking.domain.PrimaryTransaction;
import com.onlinebanking.domain.SavingsAccount;
import com.onlinebanking.domain.SavingsTransaction;
import com.onlinebanking.domain.User;
import com.onlinebanking.service.AccountService;
import com.onlinebanking.service.TransactionService;
import com.onlinebanking.service.UserService;

import com.onlinebanking.domain.CreditAccount;
import com.onlinebanking.domain.CreditTransaction;
import com.onlinebanking.dao.CreditAccountDao;

@Service
public class AccountServiceImpl implements AccountService {
	
	private static int nextAccountNumber = 11223159;

    @Autowired
    private PrimaryAccountDao primaryAccountDao;

    @Autowired
    private SavingsAccountDao savingsAccountDao;

    @Autowired
    private UserService userService;

    @Autowired
    private CreditAccountDao creditAccountDao;
    
    @Autowired
    private TransactionService transactionService;

    public PrimaryAccount createPrimaryAccount() {
        PrimaryAccount primaryAccount = new PrimaryAccount();
        primaryAccount.setAccountBalance(new BigDecimal(0.0));
        primaryAccount.setAccountNumber(accountGen());

        primaryAccountDao.save(primaryAccount);

        return primaryAccountDao.findByAccountNumber(primaryAccount.getAccountNumber());
    }

    public SavingsAccount createSavingsAccount() {
        SavingsAccount savingsAccount = new SavingsAccount();
        savingsAccount.setAccountBalance(new BigDecimal(0.0));
        savingsAccount.setAccountNumber(accountGen());

        savingsAccountDao.save(savingsAccount);

        return savingsAccountDao.findByAccountNumber(savingsAccount.getAccountNumber());
    }

    public CreditAccount createCreditAccount() {
        CreditAccount creditAccount = new CreditAccount();
        creditAccount.setAccountBalance(new BigDecimal("2000"));
        creditAccount.setAccountNumber(accountGen());

        creditAccountDao.save(creditAccount);

        return creditAccountDao.findByAccountNumber(creditAccount.getAccountNumber());
    }


    public void deposit(String accountType, double amount, Principal principal) {
        User user = userService.findByUsername(principal.getName());

        if (accountType.equalsIgnoreCase("Primary")) {
            PrimaryAccount primaryAccount = user.getPrimaryAccount();
            primaryAccount.setAccountBalance(primaryAccount.getAccountBalance().add(new BigDecimal(amount)));
            primaryAccountDao.save(primaryAccount);

            Date date = new Date();

            PrimaryTransaction primaryTransaction = new PrimaryTransaction(date, "Deposit to Primary Account", "Account", "Finished", amount, primaryAccount.getAccountBalance(), primaryAccount);
            transactionService.savePrimaryDepositTransaction(primaryTransaction);
            
        } else if (accountType.equalsIgnoreCase("Savings")) {
            SavingsAccount savingsAccount = user.getSavingsAccount();
            savingsAccount.setAccountBalance(savingsAccount.getAccountBalance().add(new BigDecimal(amount)));
            savingsAccountDao.save(savingsAccount);

            Date date = new Date();
            SavingsTransaction savingsTransaction = new SavingsTransaction(date, "Deposit to savings Account", "Account", "Finished", amount, savingsAccount.getAccountBalance(), savingsAccount);
            transactionService.saveSavingsDepositTransaction(savingsTransaction);
        }
    }
    
    public void withdraw(User user, String accountType, double amount, Principal principal) {


        if (accountType.equalsIgnoreCase("Primary")) {
            PrimaryAccount primaryAccount = user.getPrimaryAccount();
            primaryAccount.setAccountBalance(primaryAccount.getAccountBalance().subtract(new BigDecimal(amount)));
            primaryAccountDao.save(primaryAccount);

            Date date = new Date();

            PrimaryTransaction primaryTransaction = new PrimaryTransaction(date, "Withdraw from Primary Account", "Account", "Finished", amount, primaryAccount.getAccountBalance(), primaryAccount);
            transactionService.savePrimaryWithdrawTransaction(primaryTransaction);
        } else if (accountType.equalsIgnoreCase("Savings")) {
            SavingsAccount savingsAccount = user.getSavingsAccount();
            savingsAccount.setAccountBalance(savingsAccount.getAccountBalance().subtract(new BigDecimal(amount)));
            savingsAccountDao.save(savingsAccount);

            Date date = new Date();
            SavingsTransaction savingsTransaction = new SavingsTransaction(date, "Withdraw from savings Account", "Account", "Finished", amount, savingsAccount.getAccountBalance(), savingsAccount);
            transactionService.saveSavingsWithdrawTransaction(savingsTransaction);
        }
        else if (accountType.equalsIgnoreCase("Credit")) {
            CreditAccount creditAccount = user.getCreditAccount();
            creditAccount.setAccountBalance(creditAccount.getAccountBalance().subtract(new BigDecimal(amount)));
            creditAccountDao.save(creditAccount);

            Date date = new Date();

            CreditTransaction creditTransaction = new CreditTransaction(date, "Withdraw from Credit Account", amount, creditAccount.getAccountBalance(), creditAccount);
            transactionService.saveCreditWithdrawTransaction(creditTransaction);
        }
    }
    
    private int accountGen() {
        return ++nextAccountNumber;
    }

	

}
