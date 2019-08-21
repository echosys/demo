package com.onlinebanking.dao;

import com.onlinebanking.domain.Appointment;
import com.onlinebanking.domain.LoginHistory;
import org.springframework.data.repository.CrudRepository;

public interface LoginHistoryDao extends CrudRepository<LoginHistory, Long> {

}
