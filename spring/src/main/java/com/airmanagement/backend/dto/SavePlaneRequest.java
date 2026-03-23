package com.airmanagement.backend.dto;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class SavePlaneRequest {
    private String email;
    private String aircraftName;
}
