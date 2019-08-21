package com.onlinebanking.config;

import com.onlinebanking.dao.LoginHistoryDao;
import com.onlinebanking.dao.UserDao;
import com.onlinebanking.domain.LoginHistory;
import com.onlinebanking.domain.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;
import java.util.Date;

@Component
public class AuthSuccessHandler implements AuthenticationSuccessHandler {

    @Autowired
    private LoginHistoryDao loginHistoryDao;

    @Autowired
    private UserDao userDao;

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
                                        HttpServletResponse response, Authentication authentication)
            throws IOException, ServletException {
            if(authentication != null){
                LoginHistory loginHistory = new LoginHistory(new Date(), request.getRemoteAddr(), request.getHeader("User-Agent"), "Login", authentication.getName());

                loginHistoryDao.save(loginHistory);
            }

        response.sendRedirect("/userFront");
    }
}