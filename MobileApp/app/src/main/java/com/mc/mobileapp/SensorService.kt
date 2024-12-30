package com.mc.mobileapp

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Context
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
import java.util.Date

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
                userTrustScore = getUserTrustScore()
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
            val timestamp = Date(System.currentTimeMillis())
            val sensorData = when (event.sensor.type) {
                Sensor.TYPE_ACCELEROMETER -> SensorData(
                    x = event.values[0],
                    y = event.values[1],
                    z = event.values[2],
                    timestamp = timestamp,
                    sensorType = "accelerometer",
                    status = "added",
                    userId = userId,
                    userTrustScore = userTrustScore
                )

                Sensor.TYPE_GYROSCOPE -> SensorData(
                    x = event.values[0],
                    y = event.values[1],
                    z = event.values[2],
                    timestamp = timestamp,
                    sensorType = "gyroscope",
                    status = "added",
                    userId = userId,
                    userTrustScore = userTrustScore
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
                val call = sensorApiService.uploadSensorData(unuploadedData)
                call.enqueue(object : retrofit2.Callback<UserUpdateResponse> {
                    override fun onResponse(
                        call: retrofit2.Call<UserUpdateResponse>,
                        response: retrofit2.Response<UserUpdateResponse>
                    ) {
                        if (response.isSuccessful) {
                            Log.d("SensorService", "${response.body()}")
                            val trustScore = response.body()?.trustScore
                            if (trustScore != null) {
                                coroutineScope.launch {
                                    MainActivity.database.userDao()
                                        .updateTrustScore(userId, trustScore)
                                    unuploadedData.forEach { data ->
                                        data.status = "uploaded"
                                        MainActivity.database.sensorDataDao().update(data)
                                    }
                                    val updatedData =
                                        MainActivity.database.sensorDataDao().getUnuploadedData()
                                    if (updatedData.isEmpty()) {
                                        Log.d(
                                            "SensorService",
                                            "All data has been uploaded successfully"
                                        )
                                    } else {
                                        Log.e(
                                            "SensorService",
                                            "Some data was not updated to 'uploaded': $updatedData"
                                        )
                                    }
                                }
                            } else {
                                Log.e("SensorService", "Failed to upload data: trust score is null")
                            }
                        } else {
                            Log.e("SensorService", "Failed to upload data: ${response.errorBody()}")
                        }
                    }

                    override fun onFailure(call: retrofit2.Call<UserUpdateResponse>, t: Throwable) {
                        Log.e("SensorService", "Failed to upload data: ${t.message}")
                    }
                })

                // Check if the response contains a trust score
                //val trustScore = response.trustScore

                // Update the trust score in the Room database
                // MainActivity.database.userDao().updateTrustScore(userId = response.userId, trustScore = trustScore)

                // Mark data as "uploaded"
//                unuploadedData.forEach { data ->
//                    data.status = "uploaded"
//                    MainActivity.database.sensorDataDao().update(data)
//                }
//
//                val updatedData = MainActivity.database.sensorDataDao().getUnuploadedData()
//                if (updatedData.isEmpty()) {
//                    Log.d("SensorService", "All data has been uploaded successfully")
//                } else {
//                    Log.e("SensorService", "Some data was not updated to 'uploaded': $updatedData")
//                }
//
//                //Log.d("SensorService", "Uploaded ${unuploadedData.size} records and updated trust score to $trustScore")
//            } catch (e: Exception) {
//                Log.e("SensorService", "Failed to upload data: ${e.message}")
//            }
//        }
            } catch (e: Exception) {
                Log.e("SensorService", "Failed to upload data: ${e.message}")
            }
        } else {
            Log.d("SensorService", "No data to upload")
        }
    }
    private suspend fun getUserId(): Int {
        val sharedPreferences = getSharedPreferences("SHARED_PREFS", Context.MODE_PRIVATE)
        val email = sharedPreferences.getString("email", null)

        return email?.let {
            MainActivity.database.userDao().getUserId(it) ?: -1
        } ?: -1
    }
    private suspend fun getUserTrustScore(): Int {
        val sharedPreferences = getSharedPreferences("SHARED_PREFS", Context.MODE_PRIVATE)
        val email = sharedPreferences.getString("email", null)

        return email?.let {
            MainActivity.database.userDao().getUserTrustScore(it) ?: -1
        } ?: -1
    }

}