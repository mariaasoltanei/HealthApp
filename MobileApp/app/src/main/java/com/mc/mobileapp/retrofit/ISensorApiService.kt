package com.mc.mobileapp.retrofit

import com.mc.mobileapp.domains.SensorData
import retrofit2.http.Body
import retrofit2.http.POST

interface ISensorApiService {
    @POST("sensorData")
    suspend fun uploadSensorData(@Body data: EncryptedSensorBatchPayload)
}
