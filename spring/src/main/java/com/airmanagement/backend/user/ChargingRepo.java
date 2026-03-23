package com.airmanagement.backend.user;

import org.springframework.data.jpa.repository.JpaRepository;

public interface ChargingRepo extends JpaRepository<ChargingStation, Long> {
    
}
