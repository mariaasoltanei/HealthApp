package com.mc.mobileapp.screens

import android.content.Context
import android.util.Log
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.mc.mobileapp.R
import com.mc.mobileapp.utilities.BatteryUtils
import com.mc.mobileapp.utilities.CpuUtils
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@Composable
fun WelcomeScreen(onLoginClick: () -> Unit, onRegisterClick: () -> Unit) {
    val context = LocalContext.current //TODO: delete after testing score
    val coroutineScope = rememberCoroutineScope()
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
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = {
                    coroutineScope.launch {
                        testScore(context)
                    }
                },
            ) {
                Text(
                    text = "Test Score",
                    style = MaterialTheme.typography.bodyMedium.copy(
                        fontSize = 18.sp,
                        color = Color.White
                    )
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
            Button(
                onClick = {CpuUtils.stressAllCores(10)}
            ) {
                Text(
                    text = "Stress CPU",
                    style = MaterialTheme.typography.bodyMedium.copy(
                        fontSize = 18.sp,
                        color = Color.White
                    )
                )
            }
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
        }
    }
}
suspend fun testScore(context: Context) {
    val batteryLevel = BatteryUtils.getBatteryLevel(context)
    val batteryTemperature = BatteryUtils.getBatteryTemperature(context)

    val cpuInfo = withContext(Dispatchers.IO) {
        CpuUtils.getCpuUsageFromTop()
    }

    val cpuLine = CpuUtils.parseCpuLine(cpuInfo) ?: "N/A"

    Log.d("TestScore", "Battery level: $batteryLevel%")
    Log.d("TestScore", "Battery temperature: $batteryTemperature°C")
    Log.d("TestScore", "CPU Load: $cpuInfo")
}