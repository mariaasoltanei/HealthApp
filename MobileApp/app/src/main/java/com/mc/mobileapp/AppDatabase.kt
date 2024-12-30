package com.mc.mobileapp

import androidx.room.AutoMigration
import androidx.room.Database
import androidx.room.RoomDatabase
import com.mc.mobileapp.daos.ExerciseDataDao
import com.mc.mobileapp.daos.SensorDataDao
import com.mc.mobileapp.daos.UserDao
import com.mc.mobileapp.domains.ExerciseData
import com.mc.mobileapp.domains.SensorData
import com.mc.mobileapp.domains.User

@Database(
    entities = [User::class, SensorData::class, ExerciseData::class],
    version = 1,
    exportSchema = true,
//    autoMigrations = [
//        AutoMigration(from = 1, to = 2)
//    ]
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun sensorDataDao(): SensorDataDao
    abstract fun exerciseDataDao(): ExerciseDataDao
}
