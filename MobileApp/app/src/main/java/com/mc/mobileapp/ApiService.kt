package com.mc.mobileapp

import retrofit2.http.Body
import retrofit2.http.POST

interface ApiService {
    @POST("upload")
    suspend fun uploadSensorData(@Body data: List<SensorData>)
}
