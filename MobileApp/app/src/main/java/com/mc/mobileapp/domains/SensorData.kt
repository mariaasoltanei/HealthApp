package com.mc.mobileapp.domains

import androidx.room.Entity
import androidx.room.PrimaryKey

data class SensorData(
    val x: Float,
    val y: Float,
    val z: Float,
    val sensorType: String,
    val timestamp: Long,
    var userId: Int
)