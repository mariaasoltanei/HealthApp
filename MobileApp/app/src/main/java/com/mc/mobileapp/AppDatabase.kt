package com.mc.mobileapp

import androidx.room.AutoMigration
import androidx.room.Database
import androidx.room.DeleteColumn
import androidx.room.DeleteTable
import androidx.room.RenameTable
import androidx.room.RoomDatabase
import androidx.room.migration.AutoMigrationSpec
import com.mc.mobileapp.daos.ExerciseDataDao
import com.mc.mobileapp.daos.SensorDataDao
import com.mc.mobileapp.daos.UserDao
import com.mc.mobileapp.domains.ExerciseData
import com.mc.mobileapp.domains.SensorData
import com.mc.mobileapp.domains.User

@Database(entities = [User::class, SensorData::class, ExerciseData::class], version = 1, exportSchema = true
//    , autoMigrations = [
//    AutoMigration (from = 8, to = 9, spec = AppDatabase.DeleteTable::class)
//]
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun sensorDataDao(): SensorDataDao
    abstract fun exerciseDataDao(): ExerciseDataDao
}
