package com.onlinebanking;


import com.onlinebanking.config.EnableRoleChecking;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@EnableRoleChecking
@SpringBootApplication
public class UserFrontApplication {
	public static void main(String[] args) {
		SpringApplication.run(UserFrontApplication.class, args);
	}

}
