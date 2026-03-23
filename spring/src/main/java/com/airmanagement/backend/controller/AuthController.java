package com.airmanagement.backend.controller;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.airmanagement.backend.auth.AuthService;
import com.airmanagement.backend.config.JwtUtil;
import com.airmanagement.backend.dto.LoginRequest;
import com.airmanagement.backend.dto.LoginResponse;
import com.airmanagement.backend.dto.RegisterRequest;
import com.airmanagement.backend.dto.UserDto;

import lombok.RequiredArgsConstructor;
@RestController
@RequestMapping("/auth")
@RequiredArgsConstructor
public class AuthController {
    private final AuthService authService;
    private final JwtUtil jwtUtil;

    @PostMapping("/login")
    public LoginResponse login(@RequestBody LoginRequest request) {
        UserDto user = authService.login(request.getEmail(), request.getRawPassword());
        String token = jwtUtil.generateToken(user.getName());
        LoginResponse response = new LoginResponse();
        response.setToken(token);
        response.setUserDto(user);
        return response;
    }

    @PostMapping("/register")
    public void register(@RequestBody RegisterRequest request) {
        authService.register(
            request.getName(),
            request.getSurname(),
            request.getEmail(),
            request.getRawPassword()
        );
    }

}