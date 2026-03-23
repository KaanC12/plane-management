package com.airmanagement.backend.chargingpoint;

import java.time.LocalDate;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class AddRentalRequest {
    private String email;
    private LocalDate startDate;
    private LocalDate endDate;
    private String name;
}
