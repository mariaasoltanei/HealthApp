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
            val remoteExercises = apiService.getExercises()
            exerciseDataDao.insertExercises(remoteExercises)
            exerciseDataDao.getExercises()
        } catch (e: Exception) {
            exerciseDataDao.getExercises()
        }
    }

    suspend fun getExerciseById(id: Int): ExerciseData? {
        return exerciseDataDao.getExerciseById(id)
    }
}
