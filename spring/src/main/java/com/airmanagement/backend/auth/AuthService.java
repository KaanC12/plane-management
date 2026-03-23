package com.airmanagement.backend.auth;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import com.airmanagement.backend.dto.UserDto;
import com.airmanagement.backend.user.User;
import com.airmanagement.backend.user.UserRepo;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class AuthService {
    private final UserRepo userRepo;
    private final PasswordEncoder passwordEncoder;

    private User createNewUser(
        String name,
        String surname,
        String email,
        String passwordHash
    ) {
        User user = new User();
        user.setName(name);
        user.setSurname(surname);
        user.setPasswordHas(passwordHash);
        user.setEmail(email);
        return user;
    }

    public void register(
        String name,
        String surname,
        String email,
        String rawPassword
    ) {
        if (userRepo.existsByEmail(email)) {
            throw new RuntimeException("The email already taken.");
            
        }
        String passwordHash = passwordEncoder.encode(rawPassword);
        User newUser = createNewUser(name, surname, email, passwordHash);
        userRepo.save(newUser);
    }

    public UserDto login(String email, String rawPassword) {
        if (!userRepo.existsByEmail(email)) {
            throw new RuntimeException("User does not exist. Please register first.");
        }
        User user = userRepo.findByEmail(email);
        String passwordHash = user.getPasswordHas();
        
        boolean iasPasswordMatched = passwordEncoder.matches(rawPassword, passwordHash);

        if (!iasPasswordMatched) throw new RuntimeException("The password does not match.");

        UserDto userInfo = new UserDto();
        userInfo.setEmail(user.getEmail());
        userInfo.setName(user.getName());
        userInfo.setSurname(user.getSurname());

        return userInfo;
    } 
}