package com.mc.mobileapp.screens

import LandingViewModel
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.mc.mobileapp.UserRepository
import com.mc.mobileapp.daos.UserDao


class LandingViewModelFactory(
    private val userDao: UserDao,
    private val userId: Int
) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(LandingViewModel::class.java)) {
            return LandingViewModel(userDao, userId) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}