package com.onlinebanking.controller;

import java.math.BigDecimal;
import java.security.Principal;
import java.util.Collection;
import java.util.List;

import com.onlinebanking.config.Role;
import groovy.util.logging.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.ui.Model;
import org.springframework.ui.ModelMap;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

import com.onlinebanking.domain.PrimaryAccount;
import com.onlinebanking.domain.Recipient;
import com.onlinebanking.domain.SavingsAccount;
import com.onlinebanking.domain.User;
import com.onlinebanking.service.TransactionService;
import com.onlinebanking.service.UserService;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;

@Controller
@RequestMapping("/transfer")
@Slf4j
public class TransferController {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private TransactionService transactionService;

    @Autowired
    private UserService userService;

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/betweenAccounts", method = RequestMethod.GET)
    public String betweenAccounts(Model model) {
        model.addAttribute("transferFrom", "");
        model.addAttribute("transferTo", "");
        model.addAttribute("amount", "");

        return "betweenAccounts";
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/betweenAccounts", method = RequestMethod.POST)
    public String betweenAccountsPost(
            @ModelAttribute("transferFrom") String transferFrom,
            @ModelAttribute("transferTo") String transferTo,
            @ModelAttribute("amount") String amount,
            Principal principal
    ) throws Exception {
        User user = userService.findByUsername(principal.getName());
        PrimaryAccount primaryAccount = user.getPrimaryAccount();
        SavingsAccount savingsAccount = user.getSavingsAccount();
        transactionService.betweenAccountsTransfer(transferFrom, transferTo, amount, primaryAccount, savingsAccount);

        return "redirect:/userFront";
    }

    private boolean isOtpAuthorised(){
        boolean present = false;
        Collection<GrantedAuthority> authorities = (Collection<GrantedAuthority>) SecurityContextHolder.getContext().getAuthentication().getAuthorities();
        for(GrantedAuthority auth:authorities){
            if("OTP_AUTH".equalsIgnoreCase(auth.getAuthority())){
                present = true;
                break;
            }

        }
        return present;
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/recipient", method = RequestMethod.GET)
    public ModelAndView recipient(Model model, Principal principal) {

        boolean present = isOtpAuthorised();
        model.addAttribute("referrer", "/transfer/recipient");
        if(!present){
            return  new ModelAndView("redirect:/generateOtp",model.asMap());
        }
        List<Recipient> recipientList = transactionService.findRecipientList(principal);

        Recipient recipient = new Recipient();

        model.addAttribute("recipientList", recipientList);
        model.addAttribute("recipient", recipient);

        return new ModelAndView("recipient");
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/recipient/save", method = RequestMethod.POST)
    public String recipientPost(@ModelAttribute("recipient") Recipient recipient, Principal principal) {

        User user = userService.findByUsername(principal.getName());
        recipient.setUser(user);
        transactionService.saveRecipient(recipient);

        return "redirect:/transfer/recipient";
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/recipient/edit", method = RequestMethod.GET)
    public String recipientEdit(@RequestParam(value = "recipientName") String recipientName, Model model, Principal principal){

        Recipient recipient = transactionService.findRecipientByName(recipientName);
        List<Recipient> recipientList = transactionService.findRecipientList(principal);

        model.addAttribute("recipientList", recipientList);
        model.addAttribute("recipient", recipient);

        return "recipient";
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/recipient/delete", method = RequestMethod.GET)
    @Transactional
    public String recipientDelete(@RequestParam(value = "recipientName") String recipientName, Model model, Principal principal){

        transactionService.deleteRecipientByName(recipientName);

        List<Recipient> recipientList = transactionService.findRecipientList(principal);

        Recipient recipient = new Recipient();
        model.addAttribute("recipient", recipient);
        model.addAttribute("recipientList", recipientList);


        return "recipient";
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/toSomeoneElse",method = RequestMethod.GET)
    public String toSomeoneElse(Model model, Principal principal) {
        List<Recipient> recipientList = transactionService.findRecipientList(principal);

        model.addAttribute("recipientList", recipientList);
        model.addAttribute("accountType", "");

        return "toSomeoneElse";
    }


    @Role({"ROLE_USER"})
    @RequestMapping(value = "/toEmailPhone",method = RequestMethod.GET)
    public ModelAndView toEmailPhone(Model model, Principal principal, HttpServletRequest httpServletRequest) {
        boolean present = isOtpAuthorised();
        model.addAttribute("referrer", "/transfer/toEmailPhone");
        if(!present){
            return  new ModelAndView("redirect:/generateOtp",model.asMap());
        }
        return  new ModelAndView("toEmailPhone");
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/toEmailPhone",method = RequestMethod.POST)
    public String toEmailPhone(ModelMap model, @ModelAttribute("queryType") String queryType, @ModelAttribute("email") String email, @ModelAttribute("phone") String phone, @ModelAttribute("accountType") String accountType, @ModelAttribute("amount") String amount, Principal principal) {

        model.remove("Error");
        User user = userService.findByUsername(principal.getName());
        PrimaryAccount primaryAccount = user.getPrimaryAccount();
        SavingsAccount savingsAccount = user.getSavingsAccount();

        if ((accountType.equalsIgnoreCase("Primary") && primaryAccount.getAccountBalance().compareTo(new BigDecimal(amount)) < 0) ||
                (accountType.equalsIgnoreCase("Savings") && savingsAccount.getAccountBalance().compareTo(new BigDecimal(amount)) < 0)) {
            model.addAttribute("Error", "Amount is invalid");
            logger.info("Amount is invalid or balance in account less than input amount");
            return "toEmailPhone";
        }

        User recipient = null;

        System.out.println(queryType);
        System.out.println(email);
        System.out.println(phone);
        if("phone".equals(queryType)){
             recipient = userService.findByPhone(phone);
        }else{
             recipient = userService.findByEmail(email);
        }

        if(recipient == null){
            model.addAttribute("Error", "Recipient not present");
            logger.info("Recipient not found");
            return "toEmailPhone";
        }
        if(recipient!= null){
            System.out.println(recipient.getFirstName());
            transactionService.toSomeoneElseTransfer(recipient, accountType, amount, primaryAccount, savingsAccount);
        }

        return "redirect:/userFront";
    }

    @Role({"ROLE_USER"})
    @RequestMapping(value = "/toSomeoneElse",method = RequestMethod.POST)
    public String toSomeoneElsePost(ModelMap model, @ModelAttribute("recipientName") String recipientName, @ModelAttribute("accountType") String accountType, @ModelAttribute("amount") String amount, Principal principal) {
        User user = userService.findByUsername(principal.getName());
        Recipient recipient = transactionService.findRecipientByName(recipientName);

        PrimaryAccount primaryAccount = user.getPrimaryAccount();
        SavingsAccount savingsAccount = user.getSavingsAccount();
        if ((accountType.equalsIgnoreCase("Primary") && primaryAccount.getAccountBalance().compareTo(new BigDecimal(amount)) < 0) ||
                (accountType.equalsIgnoreCase("Savings") && savingsAccount.getAccountBalance().compareTo(new BigDecimal(amount)) < 0)) {
            model.addAttribute("Error", "Amount is invalid");
            return "toSomeoneElse";
        }

        transactionService.toSomeoneElseTransfer(recipient, accountType, amount, user.getPrimaryAccount(), user.getSavingsAccount());

        return "redirect:/userFront";
    }
}
