package com.mc.mobileapp.screens

import android.content.Context
import android.content.SharedPreferences
import android.util.Log
import androidx.compose.runtime.*
import androidx.compose.ui.platform.LocalContext
import com.mc.mobileapp.UserViewModel
import com.mc.mobileapp.domains.User

@Composable
fun RegisterScreen(
    userViewModel: UserViewModel,
    onRegisterSuccess: () -> Unit,
    onBackClick: () -> Unit
) {
    var currentStep by remember { mutableStateOf(1) }

    var context = LocalContext.current
    var sharedPreferences: SharedPreferences =
        context.getSharedPreferences("SHARED_PREFS", Context.MODE_PRIVATE)

    var firstName by remember { mutableStateOf("") }
    var lastName by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var birthDate by remember { mutableStateOf("") }
    var gender by remember { mutableStateOf("") }
    var height by remember { mutableStateOf("") }
    var weight by remember { mutableStateOf("") }
    var activityMultiplier by remember { mutableStateOf("") }

    // Shared error message
    var errorMessage by remember { mutableStateOf("") }

    when (currentStep) {
        1 -> PersonalDataScreen(
            firstName = firstName,
            lastName = lastName,
            email = email,
            password = password,
            onFirstNameChange = { firstName = it },
            onLastNameChange = { lastName = it },
            onEmailChange = { email = it },
            onPasswordChange = { password = it },
            onNext = {
                if (firstName.isBlank() || lastName.isBlank() || email.isBlank() || password.isBlank()) {
                    errorMessage = "Please fill in all fields."
                } else {
                    errorMessage = ""
                    currentStep = 2
                }
            },
            onBack = onBackClick,
            errorMessage = errorMessage
        )

        2 -> HealthDataScreen(
            birthDate = birthDate,
            gender = gender,
            height = height,
            weight = weight,
            activityMultiplier = activityMultiplier,
            onBirthDateChange = { birthDate = it },
            onGenderChange = { gender = it },
            onHeightChange = { height = it },
            onWeightChange = { weight = it },
            onActivityMultiplierChange = { activityMultiplier = it },
            onRegister = {
                if (birthDate.isBlank() || gender.isBlank() || height.isBlank() || weight.isBlank() || activityMultiplier.isBlank()) {
                    errorMessage = "Please fill in all fields."
                } else {
                    errorMessage = ""
                    val apiKey =
                        "IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7" // this is a mock API key
                    val user = User(
                        firstName = firstName,
                        lastName = lastName,
                        email = email,
                        password = password,
                        birthDate = birthDate,
                        height = height.toFloatOrNull() ?: 0f,
                        weight = weight.toFloatOrNull() ?: 0f,
                        gender = gender,
                        activityMultiplier = activityMultiplier.toFloatOrNull() ?: 1.0f,
                        trustScore = 100
                    )
                    userViewModel.registerUser(user, apiKey, onSuccess = {
                        onRegisterSuccess()
                        Log.d("RegisterScreen", "User registered successfully.")
                        sharedPreferences.edit().putString("email", email).apply()
                    }, onError = {
                        errorMessage = it
                    })
                }
            },
            onBack = { currentStep = 1 },
            errorMessage = errorMessage
        )
    }
}
