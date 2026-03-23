package com.airmanagement.backend.user;

import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepo extends JpaRepository<User, Long> {
    User findByEmail(String email);
    boolean existsByEmail(String email);
}