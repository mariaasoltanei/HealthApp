package com.mc.mobileapp

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class UserViewModel(private val repository: UserRepository) : ViewModel() {

    fun registerUser(user: User, onSuccess: () -> Unit, onError: (String) -> Unit) {
        viewModelScope.launch {
            try {
                // Check if user with the same email exists
                val existingUser = repository.loginUser(user.email, user.password)
                if (existingUser == null) {
                    repository.insertUser(user)
                    onSuccess()
                } else {
                    onError("Email already exists.")
                }
            } catch (e: Exception) {
                onError(e.message ?: "An error occurred.")
            }
        }
    }

    fun loginUser(
        email: String,
        password: String,
        onSuccess: (User) -> Unit,
        onError: (String) -> Unit
    ) {
        viewModelScope.launch {
            try {
                val user = repository.loginUser(email, password)
                if (user != null) {
                    onSuccess(user)
                } else {
                    onError("Invalid email or password.")
                }
            } catch (e: Exception) {
                onError(e.message ?: "An error occurred.")
            }
        }
    }
}

class UserViewModelFactory(private val repository: UserRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(UserViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return UserViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
