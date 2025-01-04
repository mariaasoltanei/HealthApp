package com.clientmobile.User

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "users")
data class User(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val firstName: String,
    val lastName: String,
    val email: String,
    val birthDate: String,
    val height: Float,
    val weight: Float,
    val gender: String,
    val activityMultiplier: Float
)
