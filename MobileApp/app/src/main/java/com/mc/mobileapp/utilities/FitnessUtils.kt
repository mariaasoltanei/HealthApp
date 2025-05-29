package com.mc.mobileapp.utilities

import java.time.LocalDate
import java.time.Period
import java.time.format.DateTimeFormatter

fun getAgeFromBirthDateString(birthDate: String, pattern: String = "yyyy-MM-dd"): Int {
    val formatter = DateTimeFormatter.ofPattern(pattern)
    val birth = LocalDate.parse(birthDate, formatter)
    return Period.between(birth, LocalDate.now()).years
}

fun calculateAge(birthDate: String): Int {
    return getAgeFromBirthDateString(birthDate)
}
fun calculateBMR(gender: String, weightKg: Float, heightCm: Float, ageYears: Int): Float {
    return if (gender == "Male") {
        10 * weightKg + 6.25f * heightCm - 5 * ageYears + 5
    } else {
        10 * weightKg + 6.25f * heightCm - 5 * ageYears - 161
    }
}

fun calculateTDEE(bmr: Float, activityMultiplier: Float): Float {
    return bmr * activityMultiplier
}