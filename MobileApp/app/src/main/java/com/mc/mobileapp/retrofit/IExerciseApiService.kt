package com.mc.mobileapp.retrofit

import com.mc.mobileapp.domains.ExerciseData
import retrofit2.http.GET

interface IExerciseApiService {
    @GET("activities")
    suspend fun getExercises(): List<ExerciseData>
}