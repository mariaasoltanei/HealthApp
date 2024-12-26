package com.mc.mobileapp.daos

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query

import com.mc.mobileapp.domains.ExerciseData

@Dao
interface ExerciseDataDao {
    @Query("SELECT * FROM exercise_data")
    suspend fun getAllExercises(): List<ExerciseData>

    @Insert(onConflict = OnConflictStrategy.NONE)
    suspend fun insertExercises(activities: List<ExerciseData>)

    @Query("SELECT * FROM exercise_data WHERE id = :id")
    suspend fun getExerciseById(id: String): ExerciseData?

    @Query("DELETE FROM exercise_data")
    suspend fun clearExercises()
}