package com.mc.mobileapp.domains

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "activity_data")
class ActivityData(
    @PrimaryKey val id: String,
    val activityName: String,
    val caloriesBurned: Int,
    val duration: String,
    val averageHeartRate: Int,
    val stepsTaken: Int,
    val activityDateTime: String,
    val notes: String
)
