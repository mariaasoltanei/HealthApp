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
import com.mc.mobileapp.domains.SensorData
import com.mc.mobileapp.domains.UserUpdateResponse
import com.mc.mobileapp.retrofit.ISensorApiService
import com.mc.mobileapp.retrofit.RetrofitClient
import kotlinx.coroutines.*

const val CHANNEL_ID = "SensorServiceChannel"
const val NOTIFICATION_ID = 1

class SensorService : Service(), SensorEventListener {

    private lateinit var sensorManager: SensorManager
    private var accelerometer: Sensor? = null
    private var gyroscope: Sensor? = null
    private val coroutineScope = CoroutineScope(Dispatchers.IO)
    private val sensorApiService = RetrofitClient.create(ISensorApiService::class.java)
    private var userId: Int = -1
    private var userTrustScore: Int = -1
    private val sensorDataBuffer = mutableListOf<SensorData>()

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
            userId = getUserId()
            userTrustScore = getUserTrustScore()
            while (true) {
                delay(10000)
                sendSensorDataBatch()
                userTrustScore = getUserTrustScore()
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
                    userId = userId,
                    userTrustScore = userTrustScore
                )

                Sensor.TYPE_GYROSCOPE -> SensorData(
                    x = event.values[0],
                    y = event.values[1],
                    z = event.values[2],
                    timestamp = timestamp,
                    sensorType = "gyroscope",
                    userId = userId,
                    userTrustScore = userTrustScore
                )

                else -> null
            }
            sensorData?.let { data ->
                synchronized(sensorDataBuffer) {
                    sensorDataBuffer.add(data)
                }
            }
        }
    }

    override fun onAccuracyChanged(sensor: Sensor?, accuracy: Int) {}

    private fun sendSensorDataBatch() {
        val dataToSend: List<SensorData>
        synchronized(sensorDataBuffer) {
            dataToSend = ArrayList(sensorDataBuffer)
            sensorDataBuffer.clear()
        }

        if (dataToSend.isNotEmpty()) {
            try {
                val call = sensorApiService.uploadSensorData(dataToSend)
                call.enqueue(object : retrofit2.Callback<UserUpdateResponse> {
                    override fun onResponse(
                        call: retrofit2.Call<UserUpdateResponse>,
                        response: retrofit2.Response<UserUpdateResponse>
                    ) {
                        if (response.isSuccessful) {
                            val trustScore = response.body()?.trustScore
                            if (trustScore != null) {
                                coroutineScope.launch {
                                    updateTrustScoreInRoom(trustScore)
                                }
                                Log.d(
                                    "SensorService",
                                    "Batch uploaded successfully. Updated trust score: $trustScore"
                                )
                            } else {
                                Log.e("SensorService", "Batch upload failed: Trust score is null")
                            }
                        } else {
                            Log.e(
                                "SensorService",
                                "Failed to upload data: ${response.message()}, ${response.code()}"
                            )
                        }
                    }

                    override fun onFailure(call: retrofit2.Call<UserUpdateResponse>, t: Throwable) {
                        Log.e("SensorService", "Failed to upload data: ${t.message}")
                    }
                })
            } catch (e: Exception) {
                Log.e("SensorService", "Error uploading batch: ${e.message}")
            }
        }
    }

    private suspend fun updateTrustScoreInRoom(newTrustScore: Int) {
        MainActivity.database.userDao().updateTrustScore(userId, newTrustScore)
        Log.d("SensorService", "Trust score updated in Room database: $newTrustScore")
    }

    private suspend fun getUserId(): Int {
        val sharedPreferences = getSharedPreferences("SHARED_PREFS", MODE_PRIVATE)
        val email = sharedPreferences.getString("email", null)

        return email?.let {
            MainActivity.database.userDao().getUserId(it) ?: -1
        } ?: -1
    }

    private suspend fun getUserTrustScore(): Int {
        val sharedPreferences = getSharedPreferences("SHARED_PREFS", MODE_PRIVATE)
        val email = sharedPreferences.getString("email", null)

        return email?.let {
            MainActivity.database.userDao().getUserTrustScore(it) ?: -1
        } ?: -1
    }

}