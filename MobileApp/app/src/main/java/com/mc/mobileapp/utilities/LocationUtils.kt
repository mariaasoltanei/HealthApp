package com.mc.mobileapp.utilities

import android.location.Location
import android.util.Log

object LocationUtils {

    /**
     * Returns true if the user is moving faster than a defined threshold (e.g., walking speed).
     */
    fun isUserMoving(location: Location?, speedThreshold: Float = 2.0f): Boolean {
        if (location == null || !location.hasSpeed()) return false
        return location.speed > speedThreshold  // speed in m/s
    }

    /**
     * Optional: Categorize movement level
     */
    fun getMovementLevel(location: Location?): MovementLevel {
        Log.d("TestScore", "Received location: $location")

        if (location == null) {
            Log.w("TestScore", "Location is null.")
            return MovementLevel.UNKNOWN
        }

        if (!location.hasSpeed()) {
            Log.w("TestScore", "Location has no speed data.")
            return MovementLevel.UNKNOWN
        }

        val speed = location.speed
        Log.d("TestScore", "Speed: $speed")

        return when {
            speed < 1.0 -> MovementLevel.STILL
            speed < 3.0 -> MovementLevel.WALKING
            speed < 6.0 -> MovementLevel.RUNNING
            else -> MovementLevel.DRIVING
        }
    }

    enum class MovementLevel {
        STILL, WALKING, RUNNING, DRIVING, UNKNOWN
    }
}
