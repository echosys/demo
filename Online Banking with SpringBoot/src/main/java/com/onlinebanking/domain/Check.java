package com.onlinebanking.domain;

import java.math.BigDecimal;

public class Check {
	private String CheckNum;
	private String RoutingNum;
	private String CustomerName;
	private BigDecimal Amount;
	public String getCheckNum() {
		return CheckNum;
	}
	public String getRoutingNum() {
		return RoutingNum;
	}
	public void setRoutingNum(String routingNum) {
		RoutingNum = routingNum;
	}
	public String getCustomerName() {
		return CustomerName;
	}
	public void setCustomerName(String customerName) {
		CustomerName = customerName;
	}
	public BigDecimal getAmount() {
		return Amount;
	}
	public void setAmount(BigDecimal amount) {
		Amount = amount;
	}
	public void setCheckNum(String checkNum) {
		CheckNum = checkNum;
	}
	
}
