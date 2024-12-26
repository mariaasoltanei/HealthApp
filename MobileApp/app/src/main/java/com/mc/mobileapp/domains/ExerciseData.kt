package com.mc.mobileapp.domains

import androidx.room.Entity

//@Entity(tableName = "exercise_data")
class ExerciseData(
    val activityName: String,
    val caloriesBurned: Int,
    val duration: String,
    val averageHeartRate: Int,
    val stepsTaken: Int,
    val activityDateTime: String,
    val notes: String,
    val activityIcon: String
)
