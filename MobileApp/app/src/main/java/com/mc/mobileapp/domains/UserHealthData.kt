package com.mc.mobileapp.domains

data class UserHealthData(
    val gender: String,
    val height: Float,
    val weight: Float,
    val birthDate: String,
    val activityMultiplier: Float
)