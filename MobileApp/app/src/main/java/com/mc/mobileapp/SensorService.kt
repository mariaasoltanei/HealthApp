package com.mc.mobileapp

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.hardware.Sensor
import android.hardware.SensorEvent
import android.hardware.SensorEventListener
import android.hardware.SensorManager
import android.os.Build
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat
import kotlinx.coroutines.*
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

const val CHANNEL_ID = "SensorServiceChannel"
const val NOTIFICATION_ID = 1
//TODO: improve requests
const val SERVER_URL = "http://192.168.0.100:5000/"

class SensorService : Service(), SensorEventListener {

    private lateinit var sensorManager: SensorManager
    private var accelerometer: Sensor? = null
    private var gyroscope: Sensor? = null
    private val coroutineScope = CoroutineScope(Dispatchers.IO)
    private val retrofit = Retrofit.Builder()
        .baseUrl(SERVER_URL)
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    private val apiService = retrofit.create(ApiService::class.java)

    override fun onCreate() {
        super.onCreate()

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                "Sensor Service",
                NotificationManager.IMPORTANCE_LOW
            )
            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannel(channel)
        }

        val notification: Notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle("Sensor Service")
            .setContentText("Logging accelerometer and gyroscope data.")
            .setSmallIcon(android.R.drawable.ic_menu_compass)
            .build()

        startForeground(NOTIFICATION_ID, notification)

        sensorManager = getSystemService(SENSOR_SERVICE) as SensorManager
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER)
        gyroscope = sensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE)

        accelerometer?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }

        gyroscope?.let {
            sensorManager.registerListener(this, it, SensorManager.SENSOR_DELAY_NORMAL)
        }

        coroutineScope.launch {
            while (true) {
                delay(10000)
                uploadUnuploadedData()
            }
        }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        return START_STICKY
    }

    override fun onDestroy() {
        super.onDestroy()
        sensorManager.unregisterListener(this)
        coroutineScope.cancel()
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }

    override fun onSensorChanged(event: SensorEvent?) {
        event?.let {
            val timestamp = System.currentTimeMillis()
            val sensorData = when (event.sensor.type) {
                Sensor.TYPE_ACCELEROMETER -> SensorData(
                    x = event.values[0],
                    y = event.values[1],
                    z = event.values[2],
                    timestamp = timestamp,
                    sensorType = "accelerometer",
                    status = "added"
                )

                Sensor.TYPE_GYROSCOPE -> SensorData(
                    x = event.values[0],
                    y = event.values[1],
                    z = event.values[2],
                    timestamp = timestamp,
                    sensorType = "gyroscope",
                    status = "added"
                )

                else -> null
            }
            sensorData?.let { data ->
                coroutineScope.launch {
                    try {
                        MainActivity.database.sensorDataDao().insert(data)
                        Log.d("SensorService", "Data inserted: $data")
                    } catch (e: Exception) {
                        Log.e("SensorService", "Failed to insert data: ${e.message}")
                    }
                }
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    private suspend fun uploadUnuploadedData() {
        val unuploadedData = MainActivity.database.sensorDataDao().getUnuploadedData()
        if (unuploadedData.isNotEmpty()) {
            try {
                apiService.uploadSensorData(unuploadedData)
                unuploadedData.forEach { data ->
                    data.status = "uploaded"
                    MainActivity.database.sensorDataDao()
                        .update(data)
                }

                val updatedData = MainActivity.database.sensorDataDao().getUnuploadedData()
                if (updatedData.isEmpty()) {
                    Log.d("SensorService", "All data has been uploaded successfully")
                } else {
                    Log.e("SensorService", "Some data was not updated to 'uploaded': $updatedData")
                }

                Log.d("SensorService", "Uploaded ${unuploadedData.size} records")
            } catch (e: Exception) {
                Log.e("SensorService", "Failed to upload data: ${e.message}")
            }
        }
    }
}