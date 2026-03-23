package com.airmanagement.backend.user;

import org.springframework.data.jpa.repository.JpaRepository;

public interface RentalRepo extends JpaRepository<Rental, Long>{
    Rental findByUser(User user); 
}
