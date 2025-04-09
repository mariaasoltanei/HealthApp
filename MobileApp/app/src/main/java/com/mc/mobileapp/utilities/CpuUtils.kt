package com.mc.mobileapp.utilities// Change to match your actual package name

import android.util.Log
import java.io.BufferedReader
import java.io.InputStreamReader

object CpuUtils {

    fun getCpuUsageFromTop(): String {
        return try {
            val process = Runtime.getRuntime().exec("top -n 1 -o PID,%CPU")
            //val reader = process.inputStream.bufferedReader()
            val bufferedReader = BufferedReader(InputStreamReader(process.inputStream))
            var line = bufferedReader.readLine()
            while (line != null) {
                Log.d("CpuUtils", line)
                line = bufferedReader.readLine()
            }
//            Log.d("CpuUtils", "Raw CPU top:\n$rawOutput")
//            val cleaned = cleanTopOutput(rawOutput)
//            Log.d("CpuUtils", "Cleaned CPU top:\n$cleaned")
            "random"
        } catch (e: Exception) {
            Log.e("CpuUtils", "Error running top: ${e.message}")
            ""
        }
    }

    private fun cleanTopOutput(raw: String): String {
        val ansiRegex = Regex("\u001B\\[[;\\d]*[A-Za-z]")
        return raw.replace(ansiRegex, "")
    }

    fun parseCpuLine(output: String): String? {
        return output
            .lines()
            .firstOrNull { it.contains("cpu") && it.contains("idle") }
            ?.trim()
    }

    fun stressAllCores(seconds: Int) {
        val numCores = Runtime.getRuntime().availableProcessors()
        repeat(numCores) { core ->
            Thread {
                val end = System.currentTimeMillis() + seconds * 1000
                while (System.currentTimeMillis() < end) {
                    var x = 0.0
                    for (i in 1..5_000_000) {
                        x += Math.sqrt(i.toDouble())
                    }
                }
                Log.d("CPU_STRESS", "Core $core done")
            }.start()
        }
    }



}
