package com.mc.mobileapp.domains

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.Date

@Entity(tableName = "sensor_data")
data class SensorData(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val userId: Int,
    val userTrustScore: Int,
    val x: Float,
    val y: Float,
    val z: Float,
    val sensorType: String,
    val timestamp: Date,
    var status: String // "added" or "uploaded"
)
