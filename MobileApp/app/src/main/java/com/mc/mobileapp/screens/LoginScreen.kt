package com.mc.mobileapp.screens

import android.util.Log
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Lock
import androidx.compose.material3.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.input.VisualTransformation
import androidx.compose.ui.unit.dp
import com.mc.mobileapp.UserViewModel
import com.mc.mobileapp.domains.User

@Composable
fun LoginScreen(
    userViewModel: UserViewModel,
    onLoginSuccess: (User) -> Unit,
    onBackClick: () -> Unit
) {
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var errorMessage by remember { mutableStateOf("") }
    var passwordVisible by remember { mutableStateOf(false) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        TextField(
            value = email,
            onValueChange = { email = it },
            label = { Text("Email") },
            modifier = Modifier.fillMaxWidth()
        )

        TextField(
            value = password,
            onValueChange = { password = it },
            label = { Text("Password") },
            visualTransformation = if (passwordVisible) VisualTransformation.None else PasswordVisualTransformation(),
            trailingIcon = {
                IconButton(onClick = { passwordVisible = !passwordVisible }) {
                    Icon(
                        imageVector = if (passwordVisible) Icons.Default.Lock else Icons.Default.Close,
                        contentDescription = if (passwordVisible) "Hide Password" else "Show Password"
                    )
                }
            },
            modifier = Modifier.fillMaxWidth()
        )

        Button(
            onClick = {
                if (email.isNotBlank() && password.isNotBlank()) {
                    userViewModel.loginUser(
                        email = email,
                        password = password,
                        apiKey = "IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7",
                        onSuccess = { user ->
                            onLoginSuccess(user)
                            Log.d("LoginScreen", "User: $user")
                        },
                        onError = { error ->
                            errorMessage = error
                        }
                    )
                } else {
                    errorMessage = "Please enter both email and password."
                }
            },
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Login")
        }
        Button(
            onClick = onBackClick,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back")
        }

        if (errorMessage.isNotBlank()) {
            Text(
                text = errorMessage,
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.padding(top = 8.dp)
            )
        }
    }
}