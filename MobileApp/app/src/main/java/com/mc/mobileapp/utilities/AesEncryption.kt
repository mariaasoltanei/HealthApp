package com.mc.mobileapp.utilities

import android.content.Context
import android.util.Base64
import android.util.Log
import java.io.IOException
import javax.crypto.Cipher
import javax.crypto.SecretKey
import javax.crypto.spec.GCMParameterSpec
import javax.crypto.spec.SecretKeySpec

object AesEncryption {

    private const val AES_MODE = "AES/GCM/NoPadding"
    private const val KEY_FILE_NAME = "aes_key.txt" // Must be in assets folder
    private var secretKey: SecretKey? = null

    fun loadKeyFromAssets(context: Context) {
        if (secretKey != null) return

        try {
            val inputStream = context.assets.open(KEY_FILE_NAME)
            val base64Key = inputStream.bufferedReader().use { it.readText().trim() }
            val keyBytes = Base64.decode(base64Key, Base64.DEFAULT)
            secretKey = SecretKeySpec(keyBytes, 0, keyBytes.size, "AES")
            Log.d("AesEncryption", "AES key loaded from assets.")
        } catch (e: IOException) {
            Log.e("AesEncryption", "Error loading AES key: ${e.message}")
        } catch (e: Exception) {
            Log.e("AesEncryption", "Unexpected error: ${e.message}")
        }
    }

    fun encrypt(data: String): Pair<String, String> {
        if (secretKey == null) {
            throw IllegalStateException("AES key not loaded. Call loadKeyFromAssets() first.")
        }

        val cipher = Cipher.getInstance(AES_MODE)
        cipher.init(Cipher.ENCRYPT_MODE, secretKey)
        val iv = cipher.iv
        val encrypted = cipher.doFinal(data.toByteArray(Charsets.UTF_8))

        val encryptedBase64 = Base64.encodeToString(encrypted, Base64.NO_WRAP)
        val ivBase64 = Base64.encodeToString(iv, Base64.NO_WRAP)

        return Pair(encryptedBase64, ivBase64)
    }
}
