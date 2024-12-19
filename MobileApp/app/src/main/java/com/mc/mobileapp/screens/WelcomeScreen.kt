package com.mc.mobileapp.screens

import android.content.Context
import android.content.Intent
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.mc.mobileapp.R
import com.mc.mobileapp.SensorService

@Composable
fun WelcomeScreen(onLoginClick: () -> Unit, onRegisterClick: () -> Unit) {
    val context = LocalContext.current
    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        Column(
            modifier = Modifier.fillMaxSize(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Image(
                painter = painterResource(id = R.drawable.ic_app_name_logo),
                contentDescription = "Fitness Icon",
                modifier = Modifier
                    .size(256.dp)
            )
        }

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .align(Alignment.BottomCenter)
                .padding(bottom = 16.dp),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            Button(
                onClick = onLoginClick,
                modifier = Modifier
                    .weight(1f)
                    .padding(end = 8.dp)
            ) {
                Text("Login")
            }

            Button(
                onClick = onRegisterClick,
                modifier = Modifier
                    .weight(1f)
                    .padding(start = 8.dp)
            ) {
                Text("Register")
            }
            Button(
                onClick = { StartAccelerometerService(context) },
                modifier = Modifier
                    .weight(1f)
                    .padding(start = 8.dp)
            ) {
                Text("Start Accelerometer")
            }
            Button(
                onClick = { StopAccelerometerService(context) },
                modifier = Modifier
                    .weight(1f)
                    .padding(start = 8.dp)
            ) {
                Text("Stop Accelerometer")
            }
        }
    }
}
fun StartAccelerometerService(context: Context) {
    val intent = Intent(context, SensorService::class.java)
    context.startService(intent)
}

fun StopAccelerometerService(context: Context) {
    val intent = Intent(context, SensorService::class.java)
    context.stopService(intent)
}