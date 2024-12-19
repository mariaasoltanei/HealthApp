package com.mc.mobileapp

import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.util.Log
import android.app.Notification
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import androidx.compose.foundation.layout.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.core.app.NotificationCompat
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent

// Constants
const val CHANNEL_ID = "SensorServiceChannel"
const val NOTIFICATION_ID = 1

// Service class
class SensorService : Service(), SensorEventListener {

    private lateinit var sensorManager: SensorManager
    private var accelerometer: Sensor? = null
    private var gyroscope: Sensor? = null

    override fun onCreate() {
        super.onCreate()

        // Create notification channel for foreground service
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Sensor Service",
                NotificationManager.IMPORTANCE_LOW
            )
            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }

        // Create notification
        val notification: Notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Sensor Service")
            .setContentText("Logging accelerometer and gyroscope data.")
            .setSmallIcon(android.R.drawable.ic_menu_compass)
            .build()

        // Start foreground service
        startForeground(NOTIFICATION_ID, notification)

        // Set up sensors
        sensorManager = getSystemService(Context.SENSOR_SERVICE) as SensorManager
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)

        accelerometer?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }

        gyroscope?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        return START_STICKY
    }

    override fun onDestroy() {
        super.onDestroy()
        sensorManager.unregisterListener(this)
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }

    override fun onSensorChanged(event: SensorEvent?) {
        event?.let {
            when (event.sensor.type) {
                Sensor.TYPE_ACCELEROMETER -> {
                    Log.d("SensorService", "Accelerometer: x=${event.values[0]} y=${event.values[1]} z=${event.values[2]}")
                }
                Sensor.TYPE_GYROSCOPE -> {
                    Log.d("SensorService", "Gyroscope: x=${event.values[0]} y=${event.values[1]} z=${event.values[2]}")
                }
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {
        // Not used in this implementation
    }
}