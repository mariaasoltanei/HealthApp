package com.mc.mobileapp.retrofit

import com.mc.mobileapp.domains.ExerciseData
import retrofit2.http.GET
import retrofit2.http.Headers

interface IExerciseApiService {
    @Headers("X-API-Key: IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7")
    @GET("activities")
    suspend fun getExercises(): List<ExerciseData>
}