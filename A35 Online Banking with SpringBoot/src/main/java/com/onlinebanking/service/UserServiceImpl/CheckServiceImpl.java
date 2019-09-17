package com.onlinebanking.service.UserServiceImpl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import com.onlinebanking.service.EmployeeService;
import java.util.List;

import com.onlinebanking.domain.User;
import com.onlinebanking.domain.PrimaryAccount;
import java.security.Principal;
import java.math.BigDecimal;
import java.util.Random;
import com.onlinebanking.service.CheckService;
import com.onlinebanking.service.UserService;

@Service
public class CheckServiceImpl implements CheckService {
    @Autowired
    private CheckService checkService;

    @Autowired
    private UserService userService;

    public void storeCheck(String checkNum, String routingNum, String customerName, BigDecimal amount){

    }

    public String IssueCheck(String AccountType, String username, double amount, Principal principal) {
        Random rand = new Random();
        int n1= 10000000+rand.nextInt(90000000);//check-number
        int n2= 896437693 ;//routing-number
        String s1= Integer.toString(n1);
        String s2= Integer.toString(n2);
        User user = userService.findByUsername(principal.getName());
        PrimaryAccount primaryAccount = user.getPrimaryAccount();
        BigDecimal balance=primaryAccount.getAccountBalance();
        BigDecimal B= new BigDecimal(amount);
        int r= B.compareTo(balance);
        if(r==1) {
            checkService.storeCheck(s1,s2,username,B);
            return "Check can be issued.Pay 3$ fee.";
        }
        else if(r==-1)
            return "Check cannot be issued.Insufficient Balance.";
        else
            return "Do you need a cheque for entire amount in account?";
    }
}


