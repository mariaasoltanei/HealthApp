package com.mc.mobileapp.domains

data class SensorData(
    val userId: Int,
    val userTrustScore: Int,
    val x: Float,
    val y: Float,
    val z: Float,
    val sensorType: String,
    val timestamp: Long,
)
