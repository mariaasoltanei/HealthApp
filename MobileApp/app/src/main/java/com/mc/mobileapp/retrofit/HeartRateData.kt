package com.mc.mobileapp.retrofit

data class HeartRateData(
    val heartRate: Int,
    val timestamp: Long,
    val userId: Int
)

data class HeartRateBatchPayload(
    val data: List<HeartRateData>,
    val timestamp: Long,
    val context: ContextInfo
)
