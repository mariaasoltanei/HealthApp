//package com.mc.mobileapp.screens
//
//import android.content.Context
//import androidx.datastore.preferences.core.Preferences
//import androidx.datastore.preferences.core.floatPreferencesKey
//import androidx.datastore.preferences.core.stringPreferencesKey
//import androidx.datastore.preferences.preferencesDataStore
//import com.mc.mobileapp.data.UserHealthData
//import kotlinx.coroutines.flow.Flow
//import kotlinx.coroutines.flow.map
//
//private val Context.dataStore by preferencesDataStore(name = "user_prefs")
//
//class UserPreferencesRepository(private val context: Context) {
//
//    companion object {
//        private val GENDER_KEY = stringPreferencesKey("gender")
//        private val HEIGHT_KEY = floatPreferencesKey("height")
//        private val WEIGHT_KEY = floatPreferencesKey("weight")
//        private val BIRTHDATE_KEY = stringPreferencesKey("birth_date")
//        private val ACTIVITY_MULTIPLIER_KEY = floatPreferencesKey("activity_multiplier")
//    }
//
//    fun getUserHealthData(): Flow<UserHealthData?> {
//        return context.dataStore.data.map { prefs ->
//            val gender = prefs[GENDER_KEY] ?: return@map null
//            val height = prefs[HEIGHT_KEY] ?: return@map null
//            val weight = prefs[WEIGHT_KEY] ?: return@map null
//            val birthDate = prefs[BIRTHDATE_KEY] ?: return@map null
//            val multiplier = prefs[ACTIVITY_MULTIPLIER_KEY] ?: return@map null
//
//            UserHealthData(
//                gender = gender,
//                height = height,
//                weight = weight,
//                birthDate = birthDate,
//                activityMultiplier = multiplier
//            )
//        }
//    }
//}
