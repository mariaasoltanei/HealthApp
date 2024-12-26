package com.mc.mobileapp.domains

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "exercise_data")
class ExerciseData(
    @PrimaryKey val id: String,
    val activityName: String,
    val caloriesBurned: Int,
    val duration: String,
    val averageHeartRate: Int,
    val stepsTaken: Int,
    val activityDateTime: String,
    val notes: String,
    val activityIcon: String,
)
