package com.mc.mobileapp

import com.mc.mobileapp.daos.UserDao
import com.mc.mobileapp.domains.User

class UserRepository(private val userDao: UserDao) {

    suspend fun insertUser(user: User) {
        userDao.insertUser(user)
    }

    suspend fun loginUser(email: String, password: String): User? {
        return userDao.findUserEmailPassword(email, password)
    }
}
