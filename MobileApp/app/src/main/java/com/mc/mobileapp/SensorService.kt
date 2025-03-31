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
import com.mc.mobileapp.retrofit.ContextInfo
import com.mc.mobileapp.retrofit.EncryptedSensorBatchPayload

import com.mc.mobileapp.retrofit.ISensorApiService
import com.mc.mobileapp.retrofit.RetrofitClient
import com.mc.mobileapp.retrofit.SensorDataEncrypted
import com.mc.mobileapp.utilities.AesEncryption
import kotlinx.coroutines.*

const val CHANNEL_ID = "SensorServiceChannel"
const val NOTIFICATION_ID = 1

class SensorService : Service(), SensorEventListener {

    private lateinit var sensorManager: SensorManager
    private var accelerometer: Sensor? = null
    private var gyroscope: Sensor? = null
    private val coroutineScope = CoroutineScope(Dispatchers.IO)
    private val sensorApiService = RetrofitClient.create(ISensorApiService::class.java)
    private val sensorDataBuffer = mutableListOf<SensorData>()
    private var userId: Int = -1

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
            while (true) {
                delay(5000)
                sendSensorDataBatch()
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
                    userId = userId
                )

                Sensor.TYPE_GYROSCOPE -> SensorData(
                    x = event.values[0],
                    y = event.values[1],
                    z = event.values[2],
                    timestamp = timestamp,
                    sensorType = "gyroscope",
                    userId = userId
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

    private suspend fun sendSensorDataBatch() {
        val dataToSend: List<SensorData>
        synchronized(sensorDataBuffer) {
            dataToSend = ArrayList(sensorDataBuffer)
            sensorDataBuffer.clear()
        }

        if (dataToSend.isNotEmpty()) {
            try {
                AesEncryption.loadKeyFromAssets(this.applicationContext)

                val encryptedDataList = dataToSend.map { entry ->
                    val (xEnc, ivX) = AesEncryption.encrypt(entry.x.toString())
                    val (yEnc, ivY) = AesEncryption.encrypt(entry.y.toString())
                    val (zEnc, ivZ) = AesEncryption.encrypt(entry.z.toString())

                    SensorDataEncrypted(
                        sensorType = entry.sensorType,
                        timestamp = entry.timestamp,
                        userId = entry.userId,
                        x = xEnc,
                        y = yEnc,
                        z = zEnc,
                        ivX = ivX,
                        ivY = ivY,
                        ivZ = ivZ
                    )
                }

                val payload = EncryptedSensorBatchPayload(
                    data = encryptedDataList,
                    timestamp = System.currentTimeMillis(),
                    context = ContextInfo(
                        user_id = userId.toString(),
                        encryption = "aes"
                    )
                )

                sensorApiService.uploadSensorData(payload)

            } catch (e: Exception) {
                Log.e("SensorService", "Encryption or upload failed: ${e.localizedMessage}")
                e.printStackTrace()
            }
        }
    }

    private suspend fun getUserId(): Int {
        val sharedPreferences = getSharedPreferences("SHARED_PREFS", MODE_PRIVATE)
        val email = sharedPreferences.getString("email", null)

        return email?.let {
            MainActivity.database.userDao().getUserId(it) ?: -1
        } ?: -1
    }

}