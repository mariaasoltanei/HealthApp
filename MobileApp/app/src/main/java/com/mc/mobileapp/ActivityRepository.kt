package com.mc.mobileapp

import com.mc.mobileapp.daos.ActivityDataDao
import com.mc.mobileapp.domains.ActivityData
import com.mc.mobileapp.retrofit.IActivityApiService

class ActivityRepository(private val activityDao: ActivityDataDao, private val apiService: IActivityApiService) {
    suspend fun getAllActivities(): List<ActivityData> {
        val cachedActivities = activityDao.getAllActivities()
        return if (cachedActivities.isNotEmpty()) {
            cachedActivities
        } else {
            val activities = apiService.getActivities()
            activityDao.insertActivities(activities)
            activities
        }
    }

    suspend fun getActivityById(id: String): ActivityData? {
        return activityDao.getActivityById(id)
    }

    suspend fun clearActivities() {
        activityDao.clearActivities()
    }
}