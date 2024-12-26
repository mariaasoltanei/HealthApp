package com.mc.mobileapp

import android.util.Log
import com.mc.mobileapp.daos.ExerciseDataDao
import com.mc.mobileapp.domains.ExerciseData
import com.mc.mobileapp.retrofit.IExerciseApiService

class ExerciseRepository(private val exerciseDataDao: ExerciseDataDao, private val apiService: IExerciseApiService) {
    suspend fun getAllExercises(): List<ExerciseData> {
        return try {
            val remoteExercises = apiService.getExercises()
            if (remoteExercises.isNotEmpty()) {
                Log.d("ExerciseRepository", "Fetched exercises from API: ${remoteExercises.size}")
                exerciseDataDao.insertExercises(remoteExercises)
                Log.d("ExerciseRepository", "Inserted exercises into local database, ${exerciseDataDao.getAllExercises().size} exercises in total")
            }
            exerciseDataDao.getAllExercises()

        } catch (e: Exception) {
            Log.e("ExerciseRepository", "Error syncing exercises: ${e.message}")
            apiService.getExercises()
        }
    }
    suspend fun getExerciseById(id: String): ExerciseData? {
        return exerciseDataDao.getExerciseById(id)
    }

    suspend fun clearActivities() {
        exerciseDataDao.clearExercises()
    }
}