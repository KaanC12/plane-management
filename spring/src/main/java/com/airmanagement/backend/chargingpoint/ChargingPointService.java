package com.airmanagement.backend.chargingpoint;
import java.util.List;
import org.springframework.stereotype.Service;

import com.airmanagement.backend.user.ChargingRepo;
import com.airmanagement.backend.user.ChargingStation;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class ChargingPointService {
    private final ChargingRepo stationRepo;


    public List<ChargingStation> getAllStations() {
        List<ChargingStation> stations = stationRepo.findAll();

        return stations;
    }
}