package com.mc.mobileapp

import android.content.Context
import android.content.SharedPreferences
import androidx.compose.ui.platform.LocalContext
import com.mc.mobileapp.daos.UserDao
import com.mc.mobileapp.domains.User
import com.mc.mobileapp.retrofit.IUserApiService

class UserRepository(private val userDao: UserDao, private val apiService: IUserApiService) {

//    private suspend fun isApiKeyValid(apiKey: String): Boolean {
//        return try {
//            apiService.validateApiKey(apiKey)
//        } catch (e: Exception) {
//            false
//        }
//    }
    suspend fun insertUser(user: User, apiKey: String) { // apiKey: String
        userDao.insertUser(user)
//        if (isApiKeyValid(apiKey)) {
//            userDao.insertUser(user)
//        } else {
//            throw IllegalAccessException("Invalid API Key")
//        }
    }

    suspend fun loginUser(email: String, password: String, apiKey: String): User? {
        return userDao.findUserEmailPassword(email, password)

//        return if (isApiKeyValid(apiKey)) {
//            userDao.findUserEmailPassword(email, password)
//        } else {
//            throw IllegalAccessException("Invalid API Key")
//        }
    }
}
