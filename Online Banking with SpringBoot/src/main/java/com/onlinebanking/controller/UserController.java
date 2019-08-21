package com.onlinebanking.controller;

import java.security.Principal;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;

import com.onlinebanking.domain.User;
import com.onlinebanking.dao.UserAccountRequestDao;
import com.onlinebanking.service.UserService;
import com.onlinebanking.domain.UserAccountRequest;
import com.onlinebanking.service.UserAccountRequestService;

@Controller
@RequestMapping("/user")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private UserAccountRequestDao userAccountRequestDao;

    @Autowired
    private UserAccountRequestService userAccountRequestService;

    @RequestMapping(value = "/profile", method = RequestMethod.GET)
    public String profile(Principal principal, Model model) {
        User user = userService.findByUsername(principal.getName());

        model.addAttribute("user", user);

        return "profile";
    }

    @RequestMapping(value = "/profile", method = RequestMethod.POST)
    public String profilePost(@ModelAttribute("user") User newUser, Model model) {
        User user = userService.findByUsername(newUser.getUsername());
        user.setUsername(newUser.getUsername());
        user.setFirstName(newUser.getFirstName());
        user.setLastName(newUser.getLastName());
        user.setEmail(newUser.getEmail());
        user.setPhone(newUser.getPhone());

        model.addAttribute("user", user);

        userService.saveUser(user);

        return "profile";
    }

    @RequestMapping(value = "/profile/additional_account", method = RequestMethod.GET)
    public String additionalAccount(Principal principal, Model model) {
        model.addAttribute("isAdditionalAccount", true);
        User user = userService.findByUsername(principal.getName());
        model.addAttribute("user", user);

        UserAccountRequest userAccountRequest=userAccountRequestDao.findByUsername(principal.getName());

            UserAccountRequest request = new UserAccountRequest();
            request.setUsername(user.getUsername());
            request.setFirstName(user.getFirstName());
            request.setLastName(user.getLastName());
            request.setPassword(user.getPassword());
            request.setPhone(user.getPhone());
            request.setUserId(user.getUserId());
            request.setUserTypeId(user.getUserTypeId());
            userAccountRequestService.createRequest(request);
            return "successAdditionalAccount";
           // return "errorAdditionalAccount";

        }
}

