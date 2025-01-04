package com.mc.mobileapp.retrofit

import com.mc.mobileapp.domains.SensorData
import com.mc.mobileapp.domains.UserUpdateResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.Headers
import retrofit2.http.POST

interface ISensorApiService {
    @Headers("X-API-Key: IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7")
    @POST("upload")
    fun uploadSensorData(@Body data: List<SensorData>): Call<UserUpdateResponse>
}
