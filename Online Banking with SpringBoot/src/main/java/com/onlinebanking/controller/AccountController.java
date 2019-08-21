package com.onlinebanking.controller;

import java.io.*;
import java.math.BigDecimal;
import java.security.Principal;
import java.util.List;

import com.onlinebanking.config.Role;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

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
import org.springframework.web.bind.annotation.ResponseBody;
import com.google.common.io.ByteStreams;
import com.google.common.primitives.Doubles;

@Controller
@RequestMapping("/account")
public class AccountController {
	
	@Autowired
    private UserService userService;
	
	@Autowired
	private AccountService accountService;
	
	@Autowired
	private TransactionService transactionService;
	
	@RequestMapping("/primaryAccount")
	public String primaryAccount(Model model, Principal principal) {
		List<PrimaryTransaction> primaryTransactionList = transactionService.findPrimaryTransactionList(principal.getName());
		
		User user = userService.findByUsername(principal.getName());
        PrimaryAccount primaryAccount = user.getPrimaryAccount();

        model.addAttribute("primaryAccount", primaryAccount);
        model.addAttribute("primaryTransactionList", primaryTransactionList);
		
		return "primaryAccount";
	}

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/primaryAccountStat", method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<byte[]> getPrimaryStat(Principal principal) throws IOException {

        List<PrimaryTransaction> primaryTransactionList = transactionService.findPrimaryTransactionList(principal.getName());


        String filePath = System.getProperty("user.dir") + "/statements";
        String filename = "primary-" + principal.getName();
        File yourFile = new File(filePath + "/" + filename);
        yourFile.createNewFile();

        byte[] file = null;

        try {
            FileOutputStream f = new FileOutputStream(yourFile);
//            ObjectOutputStream o = new ObjectOutputStream(f);
//              ObjectOutputStream o = new ObjectOutputStream(f);
            f.write("date     description       Type:      Amount     AvailabelBalance\n".getBytes());
            for(PrimaryTransaction tran: primaryTransactionList){
                f.write(tran.toString().getBytes());
            }
//            o.close();
            f.close();
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
        } catch (IOException e) {
            System.out.println("Error initializing stream");
        }


        try {
            InputStream in = new FileInputStream(filePath + "/" + filename);
            file = ByteStreams.toByteArray(in);
        }
        catch(Exception e) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment;filename=" + filename)
                // Content-Type
                .contentType(MediaType.APPLICATION_OCTET_STREAM) //
                // Content-Lengh
                .contentLength(file.length) //
                .body(file);
    }


    @RequestMapping("/savingsAccount1")
    public String savingsAccount1(Model model, Principal principal) {

        List<PrimaryTransaction> primarylist= transactionService.showPrimaryTransactionList();

        System.out.println("PrimaryList" +"----------------------" +primarylist);
       model.addAttribute("PrimaryTransactionList", primarylist);

        return "transaction_list";
		// List<SavingsTransaction> savingsTransactionList = transactionService.findSavingsTransactionList(principal.getName());
        // User user = userService.findByUsername(principal.getName());
        // SavingsAccount savingsAccount = user.getSavingsAccount();

        // model.addAttribute("savingsAccount", savingsAccount);
        // model.addAttribute("savingsTransactionList", savingsTransactionList);

        // return "savingsAccount";
    }


    @Role({"ROLE_USER"})
    @RequestMapping(value = "/savingsAccountStat", method = RequestMethod.GET)
    public @ResponseBody
    ResponseEntity<byte[]> getSavingStat(Principal principal) throws IOException {

        List<SavingsTransaction> primaryTransactionList = transactionService.findSavingsTransactionList(principal.getName());


        String filePath = System.getProperty("user.dir") + "/statements";
        String filename = "saving-" + principal.getName();
        File yourFile = new File(filePath + "/" + filename);
        yourFile.createNewFile();

        byte[] file = null;

        try {
            FileOutputStream f = new FileOutputStream(yourFile);
            f.write("date     description       Type:      Amount     AvailabelBalance\n".getBytes());
            for(SavingsTransaction tran: primaryTransactionList){
                f.write(tran.toString().getBytes());
            }
            f.close();
        } catch (FileNotFoundException e) {
            System.out.println("File not found");
        } catch (IOException e) {
            System.out.println("Error initializing stream");
        }


        try {
            InputStream in = new FileInputStream(filePath + "/" + filename);
            file = ByteStreams.toByteArray(in);
        }
        catch(Exception e) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return ResponseEntity.ok()
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment;filename=" + filename)
                // Content-Type
                .contentType(MediaType.APPLICATION_OCTET_STREAM) //
                // Content-Lengh
                .contentLength(file.length) //
                .body(file);
    }

	@RequestMapping("/savingsAccount")
    public String savingsAccount(Model model, Principal principal) {
		List<SavingsTransaction> savingsTransactionList = transactionService.findSavingsTransactionList(principal.getName());
        User user = userService.findByUsername(principal.getName());
        SavingsAccount savingsAccount = user.getSavingsAccount();

        model.addAttribute("savingsAccount", savingsAccount);
        model.addAttribute("savingsTransactionList", savingsTransactionList);

        return "savingsAccount";
    }

    @RequestMapping("/creditAccount")
    public String creditAccount(Model model, Principal principal) {
        List<CreditTransaction> creditTransactionList = transactionService.findCreditTransactionList(principal.getName());
        User user = userService.findByUsername(principal.getName());
        CreditAccount creditAccount = user.getCreditAccount();

        model.addAttribute("creditAccount", creditAccount);
        model.addAttribute("creditTransactionList", creditTransactionList);

        return "creditAccount";
    }

    @Role({"ROLE_USER"})
	@RequestMapping(value = "/deposit", method = RequestMethod.GET)
    public String deposit(Model model) {
        model.addAttribute("accountType", "");
        model.addAttribute("amount", "");

        return "deposit";
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/deposit", method = RequestMethod.POST)
    public String depositPOST(ModelMap model, @ModelAttribute("amount") String amount, @ModelAttribute("accountType") String accountType, Principal principal) {
        if (Doubles.tryParse(amount) == null){
            model.addAttribute("Error", "Amount is invalid");
            return "deposit";
        }

        accountService.deposit(accountType, Double.parseDouble(amount), principal);

        return "redirect:/userFront";
    }


    @Role({"ROLE_USER"})
    @RequestMapping(value = "/withdraw", method = RequestMethod.GET)
    public String withdraw(Model model) {
        model.addAttribute("accountType", "");
        model.addAttribute("amount", "");

        return "withdraw";
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/withdraw", method = RequestMethod.POST)
    public String withdrawPOST(ModelMap model,  @ModelAttribute("amount") String amount, @ModelAttribute("accountType") String accountType, Principal principal) {

        User user = userService.findByUsername(principal.getName());
        PrimaryAccount primaryAccount = user.getPrimaryAccount();
        SavingsAccount savingsAccount = user.getSavingsAccount();

        if ((Doubles.tryParse(amount) == null)||(accountType.equalsIgnoreCase("Primary") && primaryAccount.getAccountBalance().compareTo(new BigDecimal(amount)) < 0) ||
                (accountType.equalsIgnoreCase("Savings") && savingsAccount.getAccountBalance().compareTo(new BigDecimal(amount)) < 0)) {
            model.addAttribute("Error", "Amount is invalid");
            return "withdraw";
        }
        accountService.withdraw(user, accountType, Double.parseDouble(amount), principal);

        return "redirect:/userFront";
    }
}
