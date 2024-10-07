package com.healthapp.clientmobile.domain.activity;

public class ActivityData {
    private String activityType;
    private double noCalories;

    public ActivityData(String activityType, double noCalories) {
        this.activityType = activityType;
        this.noCalories = noCalories;
    }

    @Override
    public String toString() {
        return "ActivityData{" +
                "activityType='" + activityType + '\'' +
                ", noCalories=" + noCalories +
                '}';
    }
}