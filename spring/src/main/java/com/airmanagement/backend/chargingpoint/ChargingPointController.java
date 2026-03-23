package com.airmanagement.backend.chargingpoint;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.airmanagement.backend.user.ChargingStation;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
@RequestMapping("/charging-point")
public class ChargingPointController {
    private final ChargingPointService chargingPointService;

    @GetMapping("/get-stations")
    public List<ChargingStation> getStations() {
        return chargingPointService.getAllStations();
    }
}