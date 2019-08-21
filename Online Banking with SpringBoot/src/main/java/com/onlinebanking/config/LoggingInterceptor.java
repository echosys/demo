package com.onlinebanking.config;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.onlinebanking.dao.UserDao;
import com.onlinebanking.domain.User;
import com.onlinebanking.enums.UserTypes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;
public class LoggingInterceptor implements HandlerInterceptor  {

    @Autowired
    private UserDao userDao;

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
            throws Exception {
        System.out.println("---Before Method Execution---");
        return true;
    }
    @Override
    public void postHandle(	HttpServletRequest request, HttpServletResponse response,
                               Object handler, ModelAndView modelAndView) throws Exception {
        System.out.println("---method executed---");
        Authentication  auth = SecurityContextHolder.getContext().getAuthentication();
        if(auth != null){
            User user = userDao.findByUsername(auth.getName());
            modelAndView.addObject("userType",UserTypes.fromInt(user.getUserTypeId()).toString() );
        }

    }
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response,
                                Object handler, Exception ex) throws Exception {
        System.out.println("---Request Completed---");
    }
}

