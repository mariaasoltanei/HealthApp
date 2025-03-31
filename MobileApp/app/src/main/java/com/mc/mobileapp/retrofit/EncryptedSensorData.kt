package com.mc.mobileapp.retrofit

data class SensorDataEncrypted(
    val sensorType: String,
    val timestamp: Long,
    val userId: Int,
    val x: String,
    val y: String,
    val z: String,
    val ivX: String,
    val ivY: String,
    val ivZ: String
)

data class EncryptedSensorBatchPayload(
    val data: List<SensorDataEncrypted>,
    val timestamp: Long, //TODO:do we need this?
    val context: ContextInfo
)

data class ContextInfo(
    val user_id: String,
    val encryption: String
)
