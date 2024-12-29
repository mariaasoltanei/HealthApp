package com.mc.mobileapp

import com.mc.mobileapp.daos.UserDao
import com.mc.mobileapp.domains.User
import com.mc.mobileapp.retrofit.IUserApiService

class UserRepository(private val userDao: UserDao, private val apiService: IUserApiService) {

    private suspend fun isApiKeyValid(apiKey: String): Boolean {
        return try {
            apiService.validateApiKey(apiKey)
        } catch (e: Exception) {
            false
        }
    }
    suspend fun insertUser(user: User, apiKey: String) {
        if (isApiKeyValid(apiKey)) {
            userDao.insertUser(user)
        } else {
            throw IllegalAccessException("Invalid API Key")
        }
    }

    suspend fun loginUser(email: String, password: String, apiKey: String): User? {
        return if (isApiKeyValid(apiKey)) {
            userDao.findUserEmailPassword(email, password)
        } else {
            throw IllegalAccessException("Invalid API Key")
        }
    }
}
