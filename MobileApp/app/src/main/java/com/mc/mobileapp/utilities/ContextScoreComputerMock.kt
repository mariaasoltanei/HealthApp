package com.mc.mobileapp.utilities

import android.util.Log

object ContextScoreComputerMock {

    // Settable mock values
    var batteryLevel: Int = 50
    var batteryTemperature: Float = 30f
    var networkType: String = "mobile_data"
    var movementLevel: LocationUtilsMock.MovementLevel = LocationUtilsMock.MovementLevel.WALKING

    fun computeMockedContextScore(): Double {
        var score = 0.0

        // Battery
        if (batteryLevel > 50) score += 0.1
        else if (batteryLevel < 50) score += 0.2

        // Temp
        if (batteryTemperature > 38) score += 0.1

        // Network
        if (networkType == "public_wifi" || networkType == "mobile_data") score += 0.2

        // Movement
        if (LocationUtilsMock.isUserMoving(movementLevel)) score += 0.2

        return score.coerceIn(0.0, 1.0)
    }

    fun decideEncryptionType(): String {
        val score = computeMockedContextScore()
        return if (score >= 0.6) "he" else "aes"
    }
}
