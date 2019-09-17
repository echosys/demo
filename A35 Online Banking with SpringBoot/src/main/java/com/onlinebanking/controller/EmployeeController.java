package com.onlinebanking.controller;

import java.security.Principal;
import java.util.List;

import com.onlinebanking.service.EmployeeService;
import com.onlinebanking.service.TransactionService;
import com.onlinebanking.service.UserService;
import com.onlinebanking.service.UserServiceImpl.EmployeeServiceImpl;
import com.onlinebanking.service.UserAccountRequestService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.onlinebanking.domain.User;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import com.onlinebanking.dao.RoleDao;
import javax.validation.Valid;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import java.security.Principal;
import java.util.HashSet;
import java.util.Set;

import com.onlinebanking.enums.UserTypes;
import com.onlinebanking.domain.User;
import com.onlinebanking.domain.security.UserRole;
import com.onlinebanking.domain.UserAccountRequest;
import com.onlinebanking.dao.UserAccountRequestDao;
import com.onlinebanking.service.AccountService;
import com.onlinebanking.dao.UserDao;

@Controller
@RequestMapping("/employee")
public class EmployeeController {

    @Autowired
    private UserService userService;

    @Autowired
    private EmployeeServiceImpl employeeService;

    @Autowired
    private AccountService accountService;

    @Autowired
    private UserDao userDao;

    @Autowired
    private UserAccountRequestDao userAccountRequestDao;

    @Autowired
    private RoleDao roleDao;

    @RequestMapping(value = "/tier2", method = RequestMethod.GET)
    public String getUI(Principal principal, Model model) {
        return "tier2Interface";
    }

    @RequestMapping(value = "/accountRequests", method = RequestMethod.GET)
    public String getAdditionaAccountRequests(Principal principal, Model model) {
        List <UserAccountRequest> account_requests=userAccountRequestDao.findByEnabled(false);
        List <UserAccountRequest> approved_requests=userAccountRequestDao.findByEnabled(true);
        System.out.println("---------------------------------------");
        System.out.println(account_requests.size());
        System.out.println(approved_requests.size());
        System.out.println("---------------------------------------");
        model.addAttribute("account_requests",account_requests);
        model.addAttribute("approved_requests",approved_requests);
        return "displayRequests";
    }

    @RequestMapping(value = "/customerAccounts", method = RequestMethod.GET)
    public String getCustomerAccounts(Principal principal, Model model) {
        List <User> customer_accounts=userDao.findByUserTypeId(3);
        model.addAttribute("customer_accounts",customer_accounts);
        return "displayCustomerAccounts";
    }

    @RequestMapping(value = "/approveRequests", method = RequestMethod.GET)
    public String approveRequests(@RequestParam(value="name")String username, Principal principal, Model model) {
        UserAccountRequest userAccountRequest=userAccountRequestDao.findByUsername(username);
        User user=userService.findByUsername(username);
        user.setSavingsAccount(accountService.createSavingsAccount());
        userAccountRequest.setEnabled(true);
        userService.saveUser(user);
        userAccountRequestDao.save(userAccountRequest);
        return "redirect:/employee/accountRequests";
    }

//    @RequestMapping(value = "/declineRequests", method = RequestMethod.GET)
//    public String declineRequests(Principal principal, Model model) {
//        UserAccountRequest userAccountRequest=userAccountRequestDao.findByUsername(principal.getName());
//        userAccountRequest.setEnabled(false);
//        userAccountRequestDao.save(userAccountRequest);
//        return "displayRequests";
//    }

    @RequestMapping(value = "/modify", method = RequestMethod.GET)
    public String modifyCustomerAccount(@RequestParam(value="name")String username, Principal principal, Model model) {
        User user=userService.findByUsername(username);
        System.out.println("------------------"+ principal.getName());
        model.addAttribute("customer", user);
        return "customerModify";
    }

    @RequestMapping(value = "/customerUpdate", method = RequestMethod.POST)
    public void modifyCustomerAccount(@ModelAttribute("customer") User newUser,Principal principal, Model model) {
        User user=userService.findByUsername(newUser.getUsername());
        System.out.println("------------------"+ newUser.getUsername()+"----------------");
        user.setUsername(newUser.getUsername());
        user.setFirstName(newUser.getFirstName());
        user.setLastName(newUser.getLastName());
        user.setEmail(newUser.getEmail());
        user.setPhone(newUser.getPhone());
        model.addAttribute("customer", user);
        userService.save(user);
        getCustomerAccounts(principal, model);
        //return "customerModify";
    }

    @RequestMapping(value = "/delete", method = RequestMethod.GET)
    public void deleteCustomerAccount(@RequestParam(value="name")String username,Principal principal, Model model) {
        User user=userService.findByUsername(principal.getName());
        userDao.delete(user);
        getCustomerAccounts(principal, model);
    }

    @RequestMapping(value = "/createCustomer", method = RequestMethod.GET)
    public String createCustomerAccount(Principal principal, Model model) {
        return "signup_customer";
    }
}