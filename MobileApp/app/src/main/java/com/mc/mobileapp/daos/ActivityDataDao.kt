package com.mc.mobileapp.daos

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.mc.mobileapp.domains.ActivityData

@Dao
interface ActivityDataDao {
    @Query("SELECT * FROM activity_data")
    suspend fun getAllActivities(): List<ActivityData>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertActivities(activities: List<ActivityData>)

    @Query("SELECT * FROM activity_data WHERE id = :id")
    suspend fun getActivityById(id: String): ActivityData?

    @Query("DELETE FROM activity_data")
    suspend fun clearActivities()
}