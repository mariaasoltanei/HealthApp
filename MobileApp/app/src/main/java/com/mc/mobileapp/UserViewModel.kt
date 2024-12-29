package com.mc.mobileapp

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.mc.mobileapp.domains.User
import kotlinx.coroutines.launch

class UserViewModel(private val repository: UserRepository) : ViewModel() {

    fun registerUser(user: User, apiKey: String, onSuccess: () -> Unit, onError: (String) -> Unit) {
        viewModelScope.launch {
            try {
                val existingUser = repository.loginUser(user.email, user.password, apiKey)
                if (existingUser == null) {
                    repository.insertUser(user, apiKey)
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
        apiKey: String,
        onSuccess: (User) -> Unit,
        onError: (String) -> Unit
    ) {
        viewModelScope.launch {
            try {
                val user = repository.loginUser(email, password, apiKey)
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
