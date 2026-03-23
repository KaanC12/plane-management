package com.airmanagement.backend.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class RegisterRequest {
    private String name;
    private String surname;
    private String email;
    private String rawPassword;
}