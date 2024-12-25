package com.mc.mobileapp.retrofit

import com.mc.mobileapp.domains.ActivityData
import retrofit2.http.GET

interface IActivityApiService {
    @GET("activities")
    suspend fun getActivities(): List<ActivityData>
}