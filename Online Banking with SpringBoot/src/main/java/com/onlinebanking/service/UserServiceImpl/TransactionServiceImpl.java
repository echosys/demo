package com.onlinebanking.service.UserServiceImpl;

import java.math.BigDecimal;
import java.security.Principal;

import java.util.Date;
import java.util.List;
import java.util.stream.Collectors;

import groovy.util.logging.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.onlinebanking.dao.PrimaryAccountDao;
import com.onlinebanking.dao.PrimaryTransactionDao;
import com.onlinebanking.dao.RecipientDao;
import com.onlinebanking.dao.SavingsAccountDao;
import com.onlinebanking.dao.SavingsTransactionDao;
import com.onlinebanking.domain.PrimaryAccount;
import com.onlinebanking.domain.PrimaryTransaction;
import com.onlinebanking.domain.Recipient;
import com.onlinebanking.domain.SavingsAccount;
import com.onlinebanking.domain.SavingsTransaction;
import com.onlinebanking.domain.User;
import com.onlinebanking.service.TransactionService;
import com.onlinebanking.service.UserService;

import com.onlinebanking.dao.CreditAccountDao;
import com.onlinebanking.dao.CreditTransactionDao;
import com.onlinebanking.domain.CreditTransaction;
import com.onlinebanking.domain.CreditAccount;

@Service
@Slf4j
public class TransactionServiceImpl implements TransactionService {
	
	@Autowired
	private UserService userService;
	
	@Autowired
	private PrimaryTransactionDao primaryTransactionDao;
	
	@Autowired
	private SavingsTransactionDao savingsTransactionDao;
	
	@Autowired
	private PrimaryAccountDao primaryAccountDao;
	
	@Autowired
	private SavingsAccountDao savingsAccountDao;
	
	@Autowired
	private RecipientDao recipientDao;

    public List<PrimaryTransaction> showPrimaryTransactionList(){
        return (List<PrimaryTransaction>) primaryTransactionDao.findAll();
        // User user = userService.findByUsername(username);
        // List<PrimaryTransaction> primaryTransactionList = user.getPrimaryAccount().getPrimaryTransactionList();

        // return primaryTransactionList;
    }

    public List<SavingsTransaction> showSavingsTransactionList(){
        return (List<SavingsTransaction>) savingsTransactionDao.findAll();
        // User user = userService.findByUsername(username);
        // List<PrimaryTransaction> primaryTransactionList = user.getPrimaryAccount().getPrimaryTransactionList();

        // return primaryTransactionList;
    }

    @Autowired
    private CreditAccountDao creditAccountDao;

    @Autowired
    private CreditTransactionDao creditTransactionDao;


    public List<CreditTransaction> findCreditTransactionList(String username){
        User user = userService.findByUsername(username);
        List<CreditTransaction> creditTransactionList = user.getCreditAccount().getcreditTransactionList();

        return creditTransactionList;
    }


    public List<PrimaryTransaction> findPrimaryTransactionList(String username){
        User user = userService.findByUsername(username);
        List<PrimaryTransaction> primaryTransactionList = user.getPrimaryAccount().getPrimaryTransactionList();

        return primaryTransactionList;
    }

    public List<SavingsTransaction> findSavingsTransactionList(String username) {
        User user = userService.findByUsername(username);
        List<SavingsTransaction> savingsTransactionList = user.getSavingsAccount().getSavingsTransactionList();

        return savingsTransactionList;
    }

    public void savePrimaryDepositTransaction(PrimaryTransaction primaryTransaction) {
        primaryTransactionDao.save(primaryTransaction);
    }

    public void saveSavingsDepositTransaction(SavingsTransaction savingsTransaction) {
        savingsTransactionDao.save(savingsTransaction);
    }
    
    public void savePrimaryWithdrawTransaction(PrimaryTransaction primaryTransaction) {
        primaryTransactionDao.save(primaryTransaction);
    }

    public void saveSavingsWithdrawTransaction(SavingsTransaction savingsTransaction) {
        savingsTransactionDao.save(savingsTransaction);
    }
    public void saveCreditWithdrawTransaction(CreditTransaction creditTransaction){
        creditTransactionDao.save(creditTransaction);
    }

    public void betweenAccountsTransfer(String transferFrom, String transferTo, String amount, PrimaryAccount primaryAccount, SavingsAccount savingsAccount) throws Exception {
        if (transferFrom.equalsIgnoreCase("Primary") && transferTo.equalsIgnoreCase("Savings")) {
            primaryAccount.setAccountBalance(primaryAccount.getAccountBalance().subtract(new BigDecimal(amount)));
            savingsAccount.setAccountBalance(savingsAccount.getAccountBalance().add(new BigDecimal(amount)));
            primaryAccountDao.save(primaryAccount);
            savingsAccountDao.save(savingsAccount);

            Date date = new Date();

            PrimaryTransaction primaryTransaction = new PrimaryTransaction(date, "Between account transfer from "+transferFrom+ "  "+ primaryAccount.getAccountNumber()+" to "+transferTo+ savingsAccount.getAccountNumber(), "Account " , "Finished", Double.parseDouble(amount), primaryAccount.getAccountBalance(), primaryAccount);
            primaryTransactionDao.save(primaryTransaction);
        } else if (transferFrom.equalsIgnoreCase("Savings") && transferTo.equalsIgnoreCase("Primary")) {
            primaryAccount.setAccountBalance(primaryAccount.getAccountBalance().add(new BigDecimal(amount)));
            savingsAccount.setAccountBalance(savingsAccount.getAccountBalance().subtract(new BigDecimal(amount)));
            primaryAccountDao.save(primaryAccount);
            savingsAccountDao.save(savingsAccount);

            Date date = new Date();

            SavingsTransaction savingsTransaction = new SavingsTransaction(date, "Between account transfer from "+transferFrom+"   "+savingsAccount.getAccountNumber()+"  to "+transferTo + primaryAccount.getAccountNumber(), "Transfer", "Finished", Double.parseDouble(amount), savingsAccount.getAccountBalance(), savingsAccount);
            savingsTransactionDao.save(savingsTransaction);
        } else {
            throw new Exception("Invalid Transfer");
        }
    }
    
    public List<Recipient> findRecipientList(Principal principal) {
        String username = principal.getName();
        List<Recipient> recipientList = recipientDao.findAll().stream() 			//convert list to stream
                .filter(recipient -> username.equals(recipient.getUser().getUsername()))	//filters the line, equals to username
                .collect(Collectors.toList());

        return recipientList;
    }

    public Recipient saveRecipient(Recipient recipient) {
        return recipientDao.save(recipient);
    }

    public Recipient findRecipientByName(String recipientName) {
        return recipientDao.findByName(recipientName);
    }

    public void deleteRecipientByName(String recipientName) {
        recipientDao.deleteByName(recipientName);
    }
    
    public void toSomeoneElseTransfer(Recipient recipient, String accountType, String amount, PrimaryAccount primaryAccount, SavingsAccount savingsAccount) {
        if (accountType.equalsIgnoreCase("Primary")) {
            primaryAccount.setAccountBalance(primaryAccount.getAccountBalance().subtract(new BigDecimal(amount)));
            primaryAccountDao.save(primaryAccount);

            Date date = new Date();

            PrimaryTransaction primaryTransaction = new PrimaryTransaction(date, "Transfer to recipient "+recipient.getName(), "Transfer", "Finished", Double.parseDouble(amount), primaryAccount.getAccountBalance(), primaryAccount);
            primaryTransactionDao.save(primaryTransaction);
        } else if (accountType.equalsIgnoreCase("Savings")) {
            savingsAccount.setAccountBalance(savingsAccount.getAccountBalance().subtract(new BigDecimal(amount)));
            savingsAccountDao.save(savingsAccount);

            Date date = new Date();

            SavingsTransaction savingsTransaction = new SavingsTransaction(date, "Transfer to recipient "+recipient.getName(), "Transfer", "Finished", Double.parseDouble(amount), savingsAccount.getAccountBalance(), savingsAccount);
            savingsTransactionDao.save(savingsTransaction);
        }

        User recipientUser = recipient.getUser();
        PrimaryAccount recipientPrimaryAccount = recipientUser.getPrimaryAccount();
        SavingsAccount  recipientSavingsAccount = recipientUser.getSavingsAccount();
        if(Integer.valueOf(recipient.getAccountNumber()) == recipientPrimaryAccount.getAccountNumber()) {
            recipientPrimaryAccount.setAccountBalance(recipientPrimaryAccount.getAccountBalance().add(new BigDecimal(amount)));
            primaryAccountDao.save(recipientPrimaryAccount);
        }
        else if(Integer.valueOf(recipient.getAccountNumber()) == recipientSavingsAccount.getAccountNumber()) {
            recipientSavingsAccount.setAccountBalance(recipientSavingsAccount.getAccountBalance().add(new BigDecimal(amount)));
            savingsAccountDao.save(recipientSavingsAccount);
        }

    }

    public void toSomeoneElseTransfer(User recipient, String accountType, String amount, PrimaryAccount primaryAccount, SavingsAccount savingsAccount) {
        if (accountType.equalsIgnoreCase("Primary")) {
            primaryAccount.setAccountBalance(primaryAccount.getAccountBalance().subtract(new BigDecimal(amount)));
            primaryAccountDao.save(primaryAccount);

            Date date = new Date();

            PrimaryTransaction primaryTransaction = new PrimaryTransaction(date, "Transfer to recipient "+recipient.getFirstName(), "Transfer", "Finished", Double.parseDouble(amount), primaryAccount.getAccountBalance(), primaryAccount);
            primaryTransactionDao.save(primaryTransaction);
        } else if (accountType.equalsIgnoreCase("Savings")) {
            savingsAccount.setAccountBalance(savingsAccount.getAccountBalance().subtract(new BigDecimal(amount)));
            savingsAccountDao.save(savingsAccount);

            Date date = new Date();

            SavingsTransaction savingsTransaction = new SavingsTransaction(date, "Transfer to recipient "+recipient.getFirstName(), "Transfer", "Finished", Double.parseDouble(amount), savingsAccount.getAccountBalance(), savingsAccount);
            savingsTransactionDao.save(savingsTransaction);
        }
        PrimaryAccount  recipientPrimaryAccount = recipient.getPrimaryAccount();
        recipientPrimaryAccount.setAccountBalance(recipientPrimaryAccount.getAccountBalance().add(new BigDecimal(amount)));
        primaryAccountDao.save(recipientPrimaryAccount);
    }
}
