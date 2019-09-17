package com.onlinebanking.domain;

import javax.persistence.*;
import java.util.Date;

@Entity
public class LoginHistory {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;
    private Date loginTime;
    private String loginIP;
    private String userAgent;
    private String type;
    private String username;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Date getLoginTime() {
        return loginTime;
    }

    public void setLoginTime(Date date) {
        this.loginTime = date;
    }

    public String getLoginIP(){return loginIP;}

    public void setLoginIP(String loginIP){ this.loginIP = loginIP;}

    public String getUsername() {
        return username;
    }

    public LoginHistory(){}

    public LoginHistory(Date loginTime, String loginIP, String userAgent, String type, String username){
            this.loginIP = loginIP;
            this.loginTime = loginTime;
            this.userAgent = userAgent;
            this.type = type;
            this.username = username;
    }

}
