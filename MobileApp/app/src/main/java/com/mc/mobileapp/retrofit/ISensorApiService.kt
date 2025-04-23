package com.mc.mobileapp.retrofit

import com.mc.mobileapp.domains.SensorData
import com.mc.mobileapp.domains.SensorDataPayload
import retrofit2.http.Body
import retrofit2.http.POST

interface ISensorApiService {
    @POST("sensorData/aes")
    suspend fun uploadSensorDataAes(@Body data: EncryptedSensorBatchPayload)

    @POST("sensorData/he")
    suspend fun uploadSensorDataHe(@Body data: SensorDataPayload)

    @POST("heartRate")
    suspend fun uploadHeartRateData(@Body data: HeartRateBatchPayload)
}
