package com.airmanagement.backend.controller;

import java.util.List;
import java.util.Map;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.airmanagement.backend.auth.PlaneService;
import com.airmanagement.backend.dto.PlaneReponse;
import com.airmanagement.backend.dto.SavePlaneRequest;

import lombok.RequiredArgsConstructor;

@RestController
@RequiredArgsConstructor
@RequestMapping("/plane")
public class PlanePathController {
    private final PlaneService planeService;

    @GetMapping("/{email}/get_planes")
    public PlaneReponse getPlanes(@PathVariable String email) {
        List<String> planes = planeService.getPlanePaths(email);
        PlaneReponse response = new PlaneReponse();
        response.setPaths(planes);

        return response;
    }

    @PostMapping("/save")
    public ResponseEntity<?> savePlane(@RequestBody SavePlaneRequest request) {
        String email = request.getEmail();
        String aircraftName = request.getAircraftName();

        planeService.addPlaneToUser(email, aircraftName);

        return ResponseEntity.status(HttpStatus.OK)
            .body(Map.of("message", "Successful"));
    }
}
