package com.mc.mobileapp.daos

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.mc.mobileapp.domains.ExerciseData

@Dao
interface ExerciseDataDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertExercises(exercises: List<ExerciseData>)

    @Query("SELECT * FROM exercise_data")
    suspend fun getExercises(): List<ExerciseData>

    @Query("SELECT * FROM exercise_data WHERE id = :id")
    suspend fun getExerciseById(id: Int): ExerciseData
}
