package com.mc.mobileapp.utilities

import android.content.Context
import android.util.Log

object ContextScoreComputer {

    fun computeContextScore(context: Context): Double {
        var score = 0.0

        // Battery
        val batteryLevel = ScoreUtils.getBatteryLevel(context)
        Log.d("ContextScoreComputer", "Battery level: $batteryLevel")
        if (batteryLevel > 50) score += 0.1
        else if (batteryLevel < 20) score += 0.2

        // Temp
        val temp = ScoreUtils.getBatteryTemperature(context)
        Log.d("ContextScoreComputer", "Battery temperature: $temp")
        if (temp > 38) score += 0.1

        // Network
        val networkType = ScoreUtils.getNetworkType(context)
        Log.d("ContextScoreComputer", "Network type: $networkType")
        if (networkType == "public_wifi" || networkType == "mobile_data") score += 0.2


        // Movement
        val movementLevel = LocationUtilsMock.MovementLevel.WALKING
        Log.d("ContextScoreComputer", "Movement level: $movementLevel")
        if (LocationUtilsMock.isUserMoving(movementLevel)) score += 0.2

        return score.coerceIn(0.0, 1.0)
    }

    fun decideEncryptionType(context: Context): String {
        return if (computeContextScore(context) >= 0.6) "he" else "aes"
    }

//    fun computeContextScoreWithHeartRate(context: Context, heartRate: Int): Double{
//        var score = computeContextScore(context)
//
//        // Heart Rate
//        if (heartRate > 100) score += 0.1
//        else if (heartRate < 60) score += 0.2
//
//        return score.coerceIn(0.0, 1.0)
//
//    }

}
