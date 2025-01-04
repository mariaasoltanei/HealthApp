package com.clientmobile

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.clientmobile.User.User
import com.clientmobile.User.UserViewModel

@Composable
fun RegisterScreen(userViewModel: UserViewModel, onRegisterSuccess: () -> Unit) {
    var firstName by remember { mutableStateOf("") }
    var lastName by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var birthDate by remember { mutableStateOf("") }
    var height by remember { mutableStateOf("") }
    var weight by remember { mutableStateOf("") }
    var gender by remember { mutableStateOf("") }
    var activityMultiplier by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        TextField(value = firstName, onValueChange = { firstName = it }, label = { Text("First Name") })
        TextField(value = lastName, onValueChange = { lastName = it }, label = { Text("Last Name") })
        TextField(value = email, onValueChange = { email = it }, label = { Text("Email") })
        TextField(value = birthDate, onValueChange = { birthDate = it }, label = { Text("Birth Date (yyyy-MM-dd)") })
        TextField(
            value = height,
            onValueChange = { height = it },
            label = { Text("Height (cm)") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
        )
        TextField(
            value = weight,
            onValueChange = { weight = it },
            label = { Text("Weight (kg)") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
        )
        TextField(value = gender, onValueChange = { gender = it }, label = { Text("Gender") })
        TextField(
            value = activityMultiplier,
            onValueChange = { activityMultiplier = it },
            label = { Text("Activity Multiplier") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number)
        )
        Button(onClick = {
            if (firstName.isNotBlank() && lastName.isNotBlank() && email.isNotBlank()) {
                val user = User(
                    firstName = firstName,
                    lastName = lastName,
                    email = email,
                    birthDate = birthDate,
                    height = height.toFloatOrNull() ?: 0f,
                    weight = weight.toFloatOrNull() ?: 0f,
                    gender = gender,
                    activityMultiplier = activityMultiplier.toFloatOrNull() ?: 1.0f
                )
                userViewModel.registerUser(user, onSuccess = {
                    onRegisterSuccess()
                }, onError = {
                    errorMessage = it
                })
            } else {
                errorMessage = "Please fill in all required fields."
            }
        }) {
            Text("Register")
        }

        if (errorMessage.isNotBlank()) {
            Text(text = errorMessage, color = MaterialTheme.colorScheme.error)
        }
    }
}
