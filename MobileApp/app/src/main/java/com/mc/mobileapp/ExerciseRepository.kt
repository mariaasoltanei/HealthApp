package com.mc.mobileapp

import com.mc.mobileapp.daos.ExerciseDataDao
import com.mc.mobileapp.domains.ExerciseData
import com.mc.mobileapp.retrofit.IExerciseApiService

class ExerciseRepository(
    private val exerciseDataDao: ExerciseDataDao,
    private val apiService: IExerciseApiService
) {
    suspend fun getAllExercises(): List<ExerciseData> {
        return try {
            // Fetch from API
            val remoteExercises = apiService.getExercises()

            // Insert into database
            exerciseDataDao.insert(remoteExercises)

            // Return updated database data
            exerciseDataDao.getExercises()
        } catch (e: Exception) {
            // If API fails, return cached data
            exerciseDataDao.getExercises()
        }
    }

    suspend fun getExerciseById(id: Int): ExerciseData? {
        return exerciseDataDao.getExerciseById(id)
    }
}
