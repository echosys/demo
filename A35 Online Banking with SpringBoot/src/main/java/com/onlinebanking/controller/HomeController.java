package com.onlinebanking.controller;

import java.security.Principal;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.Map;


import com.onlinebanking.enums.UserTypes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;

import com.onlinebanking.dao.RoleDao;
import com.onlinebanking.domain.PrimaryAccount;
import com.onlinebanking.domain.SavingsAccount;
import com.onlinebanking.domain.SavingsTransaction;
import com.onlinebanking.domain.CreditAccount;
import com.onlinebanking.domain.User;
import com.onlinebanking.domain.security.UserRole;
import com.onlinebanking.service.UserService;
import com.onlinebanking.service.TransactionService;
import com.onlinebanking.domain.PrimaryTransaction;

import com.onlinebanking.service.EmailService;
import com.onlinebanking.domain.ConfirmationToken;
import com.onlinebanking.dao.ConfirmationTokenDAO;
import com.onlinebanking.dao.UserDao;
import com.onlinebanking.service.UserAccountRequestService;

@Controller
public class HomeController {

	@Autowired
	private UserService userService;


    @Autowired
    private UserAccountRequestService userAccountRequestService;

	@Autowired
    private RoleDao roleDao;

    @Autowired
	private TransactionService transactionService;


    @Autowired
    private UserDao userDao;

    @Autowired
    private ConfirmationTokenDAO confirmationTokenDao;

    @Autowired
    private EmailService emailSenderService;

	@RequestMapping("/")
	public String home() {

	    return "redirect:/index";
	}

	// @RequestMapping("/error")
	// 	public String error() {
	// 			return "redirect:/index";
	// 	}

	@RequestMapping("/index")
    public String index() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if(auth != null){
            if(auth.getName() != null && !auth.getName().equalsIgnoreCase("anonymousUser")){
                return "redirect:userFront";
            }
        }
	    return "index";
    }
	@RequestMapping("/checkinglogs")
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

    @RequestMapping("/savingslogs")
    public String savingsAccount2(Model model, Principal principal) {

        List<SavingsTransaction> savingslist= transactionService.showSavingsTransactionList();

        System.out.println("PrimaryList" +"----------------------" +savingslist);
       model.addAttribute("SavingsTransactionList", savingslist);

        return "transaction_list_saving";
		// List<SavingsTransaction> savingsTransactionList = transactionService.findSavingsTransactionList(principal.getName());
        // User user = userService.findByUsername(principal.getName());
        // SavingsAccount savingsAccount = user.getSavingsAccount();

        // model.addAttribute("savingsAccount", savingsAccount);
        // model.addAttribute("savingsTransactionList", savingsTransactionList);

        // return "savingsAccount";
    }

	@RequestMapping(value = "/signup", method = RequestMethod.GET)
    public String signup(Model model) {
        User user = new User();
        model.addAttribute("user", user);
        return "signup";
    }



	@RequestMapping(value = "/signup", method = RequestMethod.POST)
    public String signupPost(@ModelAttribute("user") User user,  @ModelAttribute("userType") String userType, Model model) {


        if(userService.checkEmailExists(user.getEmail())){
                model.addAttribute("emailExists", true);

            return "signup";
        }else if(userService.checkUsernameExists(user.getUsername())){

                model.addAttribute("usernameExists", true);

            return "signup";
        } else {
        	 Set<UserRole> userRoles = new HashSet<>();

             System.out.println(" -----------------------------"+ userType);
            if("CUSTOMER".equals(userType)){
                userRoles.add(new UserRole(user, roleDao.findByName("ROLE_USER")));
                user.setUserTypeId(UserTypes.CUSTOMER.getType());
            }
            else if("TIER_1".equals(userType)){
                userRoles.add(new UserRole(user, roleDao.findByName("TIER_1_USER_ROLE")));
                user.setUserTypeId(UserTypes.TIER_1.getType());
            }
            else if("TIER_2".equals(userType)){
                userRoles.add(new UserRole(user, roleDao.findByName("TIER_2_USER_ROLE")));
                user.setUserTypeId(UserTypes.TIER_2.getType());
            }
            else{
                userRoles.add(new UserRole(user, roleDao.findByName("ROLE_USER")));
                user.setUserTypeId(UserTypes.MERCHANT.getType());
            }

                userService.createUser(user, userRoles);

                ConfirmationToken confirmationToken = new ConfirmationToken(user.getUsername());
                confirmationTokenDao.save(confirmationToken);
            emailSenderService.sendOtpMessage(user.getEmail(),"Complete Registration!", "To confirm your account, please click here : "
                    + "https://group8-cse545.tk/confirm-account?token=" + confirmationToken.getConfirmationToken() );
                return "registrationSuccess";
            }

    }

    @RequestMapping(value="/confirm-account", method= {RequestMethod.GET, RequestMethod.POST})
    public String confirmUserAccount(Model model, @RequestParam("token")String confirmationToken)
    {
        String r=new String();
        ConfirmationToken token = confirmationTokenDao.findByConfirmationToken(confirmationToken);

        if(token != null)
        {
            User user = userDao.findByUsername(token.getUsername());
            user.setEnabled(true);
            userDao.save(user);
            r="emailVerified";

        }
        else
        {
            r="emailVerificationError";
        }

        return r;
    }

	@RequestMapping("/userFront")
	public String userFront(Principal principal, Model model) {
        User user = userService.findByUsername(principal.getName());
        PrimaryAccount primaryAccount = user.getPrimaryAccount();
        SavingsAccount savingsAccount = user.getSavingsAccount();
        CreditAccount creditAccount=user.getCreditAccount();
        if(creditAccount==null)
            System.out.println("---------Acc NULL-----------");
        model.addAttribute("primaryAccount", primaryAccount);
        model.addAttribute("savingsAccount", savingsAccount);
        model.addAttribute("creditAccount", creditAccount);

        return "userFront";
    }
}
