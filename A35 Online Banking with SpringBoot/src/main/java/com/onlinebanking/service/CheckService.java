package com.onlinebanking.service;

import java.math.BigDecimal;
import com.onlinebanking.domain.PrimaryAccount;
import java.security.Principal;
import java.util.Random;

public interface CheckService {

	public String IssueCheck(String AccountType, String username, double amount, Principal principal);
	public void storeCheck(String checkNum, String routingNum, String customerName, BigDecimal amount);

}
