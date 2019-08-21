package com.onlinebanking.service;

import java.security.Principal;
import java.util.List;

import com.onlinebanking.domain.PrimaryAccount;
import com.onlinebanking.domain.PrimaryTransaction;
import com.onlinebanking.domain.Recipient;
import com.onlinebanking.domain.SavingsAccount;
import com.onlinebanking.domain.SavingsTransaction;
import com.onlinebanking.domain.User;
import com.onlinebanking.domain.CreditAccount;
import com.onlinebanking.domain.CreditTransaction;

public interface TransactionService {
    List<PrimaryTransaction> showPrimaryTransactionList();

    List<SavingsTransaction> showSavingsTransactionList();

	List<PrimaryTransaction> findPrimaryTransactionList(String username);

    List<SavingsTransaction> findSavingsTransactionList(String username);

    List<CreditTransaction> findCreditTransactionList(String username);

    void savePrimaryDepositTransaction(PrimaryTransaction primaryTransaction);

    void saveSavingsDepositTransaction(SavingsTransaction savingsTransaction);
    
    void savePrimaryWithdrawTransaction(PrimaryTransaction primaryTransaction);
    void saveSavingsWithdrawTransaction(SavingsTransaction savingsTransaction);
    void saveCreditWithdrawTransaction(CreditTransaction creditTransaction);
    
    void betweenAccountsTransfer(String transferFrom, String transferTo, String amount, PrimaryAccount primaryAccount, SavingsAccount savingsAccount) throws Exception;
    
    List<Recipient> findRecipientList(Principal principal);

    Recipient saveRecipient(Recipient recipient);

    Recipient findRecipientByName(String recipientName);

    void deleteRecipientByName(String recipientName);
    
    void toSomeoneElseTransfer(Recipient recipient, String accountType, String amount, PrimaryAccount primaryAccount, SavingsAccount savingsAccount);

    void toSomeoneElseTransfer(User recipient, String accountType, String amount, PrimaryAccount primaryAccount, SavingsAccount savingsAccount);

}
