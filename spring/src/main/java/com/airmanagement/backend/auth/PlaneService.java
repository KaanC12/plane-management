package com.airmanagement.backend.auth;

import org.springframework.stereotype.Service;

import com.airmanagement.backend.plane.Plane;
import com.airmanagement.backend.plane.PlaneRepo;
import com.airmanagement.backend.user.UserRepo;
import com.airmanagement.backend.user.User;

import java.util.LinkedList;
import java.util.List;

import lombok.RequiredArgsConstructor;

@Service
@RequiredArgsConstructor
public class PlaneService {
    private final UserRepo userRepo;
    private final PlaneRepo planeRepo;

    public List<String> getPlanePaths(String email) {
        List<String> paths = new LinkedList<>();
        User user = userRepo.findByEmail(email);
        List<Plane> planes = user.getPlanes();

        if (planes.size() == 0) paths.add(null);
        else{
            for (Plane plane: planes) {
                paths.add(plane.getFilePath());
            }
        }
        return paths;
    }

    public void addPlaneToUser(String email, String aircraftName) {
        User user = userRepo.findByEmail(email);
        String filePath = String.format("/uploads/planes/%s.png", aircraftName);
        Plane newPlane = new Plane();
        newPlane.setAircraftName(aircraftName);
        newPlane.setFilePath(filePath);

        planeRepo.save(newPlane);
        
        user.getPlanes().add(newPlane);
        userRepo.save(user);
    }
}
