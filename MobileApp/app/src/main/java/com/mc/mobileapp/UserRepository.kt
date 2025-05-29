package com.mc.mobileapp

import com.mc.mobileapp.daos.UserDao
import com.mc.mobileapp.domains.User
import com.mc.mobileapp.domains.UserHealthData
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

class UserRepository(private val userDao: UserDao) {
    suspend fun insertUser(user: User): Long {
        return userDao.insertUser(user)
    }

    suspend fun loginUser(email: String, password: String): User? {
        return userDao.findUserEmailPassword(email, password)
    }
}
