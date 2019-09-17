package com.onlinebanking.config;

import java.lang.annotation.Annotation;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;


import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


import com.onlinebanking.dao.UserDao;


import com.onlinebanking.domain.User;
import com.onlinebanking.enums.UserTypes;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.method.HandlerMethod;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;


@Component
public class SecurityInterceptor implements HandlerInterceptor {

    @Autowired
    private UserDao userDao;
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {



        // cast the annotated spring handler method
        HandlerMethod handlerMethod = (HandlerMethod) handler;
        // get method using reflection
        Method method = handlerMethod.getMethod();
        // check if the method is annotated
        if (handlerMethod.getMethod().isAnnotationPresent(Role.class)) {

            boolean present = false;
            String connectedUser = request.getUserPrincipal() == null ? null : request.getUserPrincipal().getName();

            // if no user is logged in, then exit
            if (connectedUser == null){
                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                return false;
            }

            Collection<GrantedAuthority> authorities = (Collection<GrantedAuthority>) SecurityContextHolder.getContext().getAuthentication().getAuthorities();
            Annotation annotation = method.getAnnotation(Role.class);
            Role casRole = (Role) annotation;

            //System.out.printf("Access :%s\n", casRole.access());
            String[] roles = casRole.value();


            List<String> UserRoleId = new ArrayList<String>();

            for(GrantedAuthority role:authorities){
                UserRoleId.add(role.getAuthority());
            }
            for(String role:roles){
                if(UserRoleId.contains(role)){
                    present = true;
                    return true;
                }
            }

            if(!present){
                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                return false;
            }


        }

        return true;
    }

    @Override
    public void postHandle(	HttpServletRequest request, HttpServletResponse response,
                               Object handler, ModelAndView modelAndView) throws Exception {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if(auth != null){
            User user = userDao.findByUsername(auth.getName());
            if(user != null && modelAndView != null)
            {
                modelAndView.addObject("userType", UserTypes.fromInt(user.getUserTypeId()).toString() );
            }
        }
        System.out.println("---method executed---");
    }
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response,
                                Object handler, Exception ex) throws Exception {
        System.out.println("---Request Completed---");
    }
}