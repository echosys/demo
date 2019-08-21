package com.onlinebanking.controller;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.onlinebanking.dao.UserDao;
import com.onlinebanking.domain.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.onlinebanking.service.EmailService;
import com.onlinebanking.service.OtpService;
import com.onlinebanking.utility.EmailTemplate;

@Controller
public class OtpController {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    public OtpService otpService;

    @Autowired
    public EmailService emailService;

    @Autowired
    private UserDao userDao;

    @GetMapping("/generateOtp")
    public String generateOtp(Model model, @RequestParam("referrer") String referrer){

        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String username = auth.getName();
        User user = userDao.findByUsername(username);

        int otp = otpService.generateOTP(username);

        logger.info("OTP : "+otp);

        //Generate The Template to send OTP
        EmailTemplate template = new EmailTemplate("SendOtp.html");

        Map<String,String> replacements = new HashMap<String,String>();
        replacements.put("user", username);
        replacements.put("otpnum", String.valueOf(otp));

        String message = template.getTemplate(replacements);
        String email = user.getEmail();

        emailService.sendOtpMessage(email, "OTP -SpringBoot", message);

        model.addAttribute("referrer", referrer);

        return "otppage";
    }

    @RequestMapping(value ="/validateOtp", method = RequestMethod.GET)
    public @ResponseBody String validateOtp(@RequestParam("otpnum") int otpnum, @RequestParam("referrer") String referer){

        final String SUCCESS = "Entered Otp is valid";

        final String FAIL = "Entered Otp is NOT valid. Please Retry!";

        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        String username = auth.getName();

        logger.info(" Otp Number : "+otpnum);

        //Validate the Otp
        if(otpnum >= 0){
            int serverOtp = otpService.getOtp(username);

            if(serverOtp > 0){
                if(otpnum == serverOtp){
                    otpService.clearOTP(username);
                    List<GrantedAuthority> updatedAuthorities = new ArrayList<GrantedAuthority>(auth.getAuthorities());
                    updatedAuthorities.add(new SimpleGrantedAuthority("OTP_AUTH")); //add your role here [e.g., new SimpleGrantedAuthority("ROLE_NEW_ROLE")]
                    Authentication newAuth = new UsernamePasswordAuthenticationToken(auth.getPrincipal(), auth.getCredentials(), updatedAuthorities);
                    SecurityContextHolder.getContext().setAuthentication(newAuth);
                    return referer;
                }else{
                    return FAIL;
                }
            }else {
                return FAIL;
            }
        }else {
            return FAIL;
        }
    }
}

