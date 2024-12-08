package com.healthapp.clientmobile.sensors;

import java.util.Date;

public class SensorData {
    private String userId;
    private float x;
    private float y;
    private float z;
    private Date timestamp;

    public SensorData() {
    }
    public SensorData(String userId, float x, float y, float z, Date timestamp) {
        this.userId = userId;
        this.x = x;
        this.y = y;
        this.z = z;
        this.timestamp = timestamp;
    }

    public String getUserId() {
        return userId;
    }

    public void setUserId(String userId) {
        this.userId = userId;
    }

    public float getX() {
        return x;
    }

    public void setX(float x) {
        this.x = x;
    }

    public float getY() {
        return y;
    }

    public void setY(float y) {
        this.y = y;
    }

    public float getZ() {
        return z;
    }

    public void setZ(float z) {
        this.z = z;
    }

    public Date getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Date timestamp) {
        this.timestamp = timestamp;
    }
}
