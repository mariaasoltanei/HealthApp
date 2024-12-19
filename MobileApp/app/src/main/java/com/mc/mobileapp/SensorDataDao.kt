package com.mc.mobileapp

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.Query
import androidx.room.Update

@Dao
interface SensorDataDao {
    @Insert
    suspend fun insert(sensorData: SensorData)

    @Query("SELECT * FROM sensor_data WHERE status = 'added'")
    suspend fun getUnuploadedData(): List<SensorData>

    @Update
    suspend fun update(sensorData: SensorData)
}