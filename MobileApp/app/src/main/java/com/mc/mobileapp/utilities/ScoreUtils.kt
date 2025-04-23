package com.mc.mobileapp.utilities

import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.net.wifi.WifiManager
import android.os.BatteryManager
import android.os.Build
import android.util.Log

object ScoreUtils {
    fun getBatteryLevel(context: Context): Int {
        val batteryIntent =
            context.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
        val level = batteryIntent?.getIntExtra(BatteryManager.EXTRA_LEVEL, -1) ?: -1
        val scale = batteryIntent?.getIntExtra(BatteryManager.EXTRA_SCALE, -1) ?: -1
        return if (level >= 0 && scale > 0) (level * 100 / scale) else 50
    }

    fun getBatteryTemperature(context: Context): Float {
        val intent = context.registerReceiver(null, IntentFilter(Intent.ACTION_BATTERY_CHANGED))
        val temp = intent?.getIntExtra(BatteryManager.EXTRA_TEMPERATURE, 0) ?: 0
        return temp / 10f // convert to Celsius
    }

    fun getNetworkType(context: Context): String {
        val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
        val network = cm.activeNetwork ?: return "none"
        val capabilities = cm.getNetworkCapabilities(network) ?: return "unknown"

        return when {
            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> {
                val ssid = getCurrentSsid(context)
                if (ssid.contains("guest", true) || ssid.contains("free")) "public_wifi"
                else "secure_wifi"
            }

            capabilities.hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> "mobile_data"
            else -> "unknown"
        }
    }

    fun getCurrentSsid(context: Context): String {
        return try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                // On Android 10+ you must use NetworkCapabilities
                val connectivityManager =
                    context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
                val network = connectivityManager.activeNetwork ?: return "unknown"
                val networkCapabilities = connectivityManager.getNetworkCapabilities(network)
                    ?: return "unknown"

                if (networkCapabilities.hasTransport(NetworkCapabilities.TRANSPORT_WIFI)) {
                    val wifiManager =
                        context.applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
                    val wifiInfo = wifiManager.connectionInfo
                    // connectionInfo is deprecated, but still gives SSID with fallback
                    wifiInfo.ssid?.removePrefix("\"")?.removeSuffix("\"") ?: "unknown"
                } else {
                    "not_wifi"
                }
            } else {
                // Pre-Android 10 fallback
                val wifiManager =
                    context.applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
                val wifiInfo = wifiManager.connectionInfo
                wifiInfo.ssid?.removePrefix("\"")?.removeSuffix("\"") ?: "unknown"
            }
        } catch (e: Exception) {
            Log.e("WifiUtils", "Failed to get SSID: ${e.message}")
            "unknown"
        }
    }
}


