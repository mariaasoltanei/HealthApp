//package com.mc.mobileapp.services
//
//import android.app.Service
//
//import android.app.NotificationChannel
//import android.app.NotificationManager
//import android.content.Intent
//import android.os.Build
//import android.os.IBinder
//import android.util.Log
//import androidx.core.app.NotificationCompat
//import com.mc.mobileapp.MainActivity
//import com.mc.mobileapp.retrofit.ContextInfo
//import com.mc.mobileapp.retrofit.HeartRateBatchPayload
//import com.mc.mobileapp.retrofit.HeartRateData
//import com.mc.mobileapp.retrofit.ISensorApiService
//import com.mc.mobileapp.retrofit.RetrofitClient
//import kotlinx.coroutines.CoroutineScope
//
//import kotlinx.coroutines.Dispatchers
//import kotlinx.coroutines.cancel
//import kotlinx.coroutines.delay
//import kotlinx.coroutines.launch
//import kotlin.collections.isNotEmpty
//
//class HeartRateService : Service() {
//
//    private val coroutineScope = CoroutineScope(Dispatchers.IO)
//    private val sensorApiService = RetrofitClient.create(ISensorApiService::class.java)
//    private val heartRateBuffer = mutableListOf<HeartRateData>()
//    private var userId: Int = -1
//
//    override fun onCreate() {
//        super.onCreate()
//
//        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
//            val channel = NotificationChannel(
//                CHANNEL_ID,
//                "Heart Rate Service",
//                NotificationManager.IMPORTANCE_LOW
//            )
//            getSystemService(NotificationManager::class.java).createNotificationChannel(channel)
//        }
//
//        val notification = NotificationCompat.Builder(this, CHANNEL_ID)
//            .setContentTitle("Heart Rate Service")
//            .setContentText("Sending heart rate data to backend.")
//            .setSmallIcon(android.R.drawable.ic_menu_info_details)
//            .build()
//
//        startForeground(NOTIFICATION_ID, notification)
//
//        coroutineScope.launch {
//            userId = getUserId()
//            while (true) {
//                simulateHeartRateReading()
//                delay(5000)
//                sendHeartRateBatch()
//            }
//        }
//    }
//
//    override fun onDestroy() {
//        super.onDestroy()
//        coroutineScope.cancel()
//    }
//
//    override fun onBind(intent: Intent?): IBinder? = null
//
//    private fun simulateHeartRateReading() {
//        val timestamp = System.currentTimeMillis()
//        val heartRate = (60..100).random()
//
//        val data = HeartRateData(
//            heartRate = heartRate,
//            timestamp = timestamp,
//            userId = userId
//        )
//
//        synchronized(heartRateBuffer) {
//            heartRateBuffer.add(data)
//        }
//    }
//
//    private suspend fun sendHeartRateBatch() {
//        val dataToSend: List<HeartRateData>
//        synchronized(heartRateBuffer) {
//            dataToSend = ArrayList(heartRateBuffer)
//            heartRateBuffer.clear()
//        }
//
//        if (dataToSend.isNotEmpty()) {
//            try {
//                val payload = HeartRateBatchPayload(
//                    data = dataToSend,
//                    timestamp = System.currentTimeMillis(),
//                    context = ContextInfo(
//                        user_id = userId.toString(),
//                        encryption = "he"
//                    )
//                )
//
//                sensorApiService.uploadHeartRateData(payload)
//
//            } catch (e: Exception) {
//                Log.e("HeartRateService", "Upload failed: ${e.localizedMessage}")
//                e.printStackTrace()
//            }
//        }
//    }
//
//    private suspend fun getUserId(): Int {
//        val sharedPreferences = getSharedPreferences("SHARED_PREFS", MODE_PRIVATE)
//        val email = sharedPreferences.getString("email", null)
//        return email?.let {
//            MainActivity.database.userDao().getUserId(it) ?: -1
//        } ?: -1
//    }
//
//    companion object {
//        private const val CHANNEL_ID = "HeartRateServiceChannel"
//        private const val NOTIFICATION_ID = 2
//    }
//}
