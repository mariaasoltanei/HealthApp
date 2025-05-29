package com.mc.mobileapp.screens

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.os.Looper
import android.util.Log
import com.google.android.gms.location.*
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
import androidx.core.content.ContextCompat
import com.google.android.gms.location.LocationCallback
import com.google.android.gms.location.LocationResult
import com.google.android.gms.location.LocationServices

import com.mc.mobileapp.R
import com.mc.mobileapp.utilities.LocationUtils
import com.mc.mobileapp.utilities.ScoreUtils
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.tasks.await
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
                painter = painterResource(id = R.drawable.icon_logo),
                contentDescription = "Fitness Icon",
                modifier = Modifier
                    .size(256.dp)
            )
            Spacer(modifier = Modifier.height(16.dp))
//            Button(
//                onClick = {
//                    coroutineScope.launch {
//                        testScore(context)
//                    }
//                },
//            ) {
//                Text(
//                    text = "Test Score",
//                    style = MaterialTheme.typography.bodyMedium.copy(
//                        fontSize = 18.sp,
//                        color = Color.White
//                    )
//                )
//            }
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
    val batteryLevel = ScoreUtils.getBatteryLevel(context)
    val batteryTemperature = ScoreUtils.getBatteryTemperature(context)

    Log.d("TestScore", "Battery level: $batteryLevel%")
    Log.d("TestScore", "Battery temperature: $batteryTemperature°C")

    // ✅ Check location permission
    val hasPermission = ContextCompat.checkSelfPermission(
        context,
        Manifest.permission.ACCESS_FINE_LOCATION
    ) == PackageManager.PERMISSION_GRANTED

    if (!hasPermission) {
        Log.w("TestScore", "Location permission not granted.")
        return
    }

    val fusedLocationClient = LocationServices.getFusedLocationProviderClient(context)

    val location = suspendCancellableCoroutine<Location?> { continuation ->
        val request = LocationRequest.Builder(
            Priority.PRIORITY_HIGH_ACCURACY,
            0L // immediate
        ).setMaxUpdates(1)
            .setMinUpdateIntervalMillis(0)
            .build()

        val callback = object : LocationCallback() {
            override fun onLocationResult(result: LocationResult) {
                fusedLocationClient.removeLocationUpdates(this)
                continuation.resume(result.lastLocation, null)
            }

            override fun onLocationAvailability(availability: LocationAvailability) {
                if (!availability.isLocationAvailable) {
                    Log.w("TestScore", "Live location not available")
                }
            }
        }
        val settingsClient = LocationServices.getSettingsClient(context)
        val locationRequest = LocationRequest.Builder(Priority.PRIORITY_HIGH_ACCURACY, 1000L).build()
        val settingsRequest = LocationSettingsRequest.Builder().addLocationRequest(locationRequest).build()

        settingsClient.checkLocationSettings(settingsRequest)
            .addOnFailureListener { e ->
                Log.e("TestScore", "Location settings not satisfied: ${e.message}")
            }

        fusedLocationClient.requestLocationUpdates(
            request,
            callback,
            Looper.getMainLooper()
        )
    }

    val isMoving = LocationUtils.isUserMoving(location)
    val movementLevel = LocationUtils.getMovementLevel(location)

    Log.d("TestScore", "Live Location: $location")
    Log.d("TestScore", "Is user moving? $isMoving")
    Log.d("TestScore", "Movement level: $movementLevel")
}