package com.healthapp.clientmobile.domain.sensors;

import java.util.Date;

public class GyroscopeData extends SensorData {
    public GyroscopeData(String userId, float x, float y, float z, Date timestamp) {
        super(userId, x, y, z, timestamp);
    }
}