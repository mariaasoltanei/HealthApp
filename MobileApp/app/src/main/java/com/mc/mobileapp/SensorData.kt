package com.mc.mobileapp

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "sensor_data")
data class SensorData(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val x: Float,
    val y: Float,
    val z: Float,
    val sensorType: String,
    val timestamp: Long,
    var status: String // "added" or "uploaded"
)
