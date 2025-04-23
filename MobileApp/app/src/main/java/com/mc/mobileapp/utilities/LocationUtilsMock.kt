package com.mc.mobileapp.utilities

object LocationUtilsMock {

    enum class MovementLevel {
        STILL, WALKING, RUNNING, UNKNOWN
    }

    fun isUserMoving(movementLevel: MovementLevel): Boolean {
        return when (movementLevel) {
            MovementLevel.STILL, MovementLevel.UNKNOWN -> false
            else -> true
        }
    }

}
