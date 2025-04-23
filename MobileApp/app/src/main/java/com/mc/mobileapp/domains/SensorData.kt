package com.mc.mobileapp.domains

import com.mc.mobileapp.retrofit.ContextInfo
import com.mc.mobileapp.retrofit.SensorDataEncrypted

data class SensorData(
    val x: Float,
    val y: Float,
    val z: Float,
    val sensorType: String,
    val timestamp: Long,
    var userId: Int
)

data class SensorDataPayload(
    val data: List<SensorData>,
    val timestamp: Long, //TODO:do we need this?
    val context: ContextInfo
)