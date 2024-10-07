package com.healthapp.clientmobile.domain.sensors;

import java.util.Date;

public class AccelerometerData extends SensorData {
    public AccelerometerData(String userId, float x, float y, float z, Date timestamp) {
        super(userId, x, y, z, timestamp);
    }
}