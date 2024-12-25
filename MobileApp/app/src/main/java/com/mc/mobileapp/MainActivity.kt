package com.mc.mobileapp

import AppNavGraph
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.navigation.compose.rememberNavController
import androidx.room.Room
import com.mc.mobileapp.retrofit.IActivityApiService
import com.mc.mobileapp.retrofit.ISensorApiService
import com.mc.mobileapp.retrofit.RetrofitClient
import com.mc.mobileapp.ui.theme.MobileAppTheme

class MainActivity : ComponentActivity() {
    companion object {
        lateinit var database: AppDatabase
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        database = Room.databaseBuilder(
            this.applicationContext,
            AppDatabase::class.java,
            "health_app_db"
        ).build()

        val userRepository = UserRepository(database.userDao())
        val activityRepository = ActivityRepository(database.activityDataDao(), apiService = RetrofitClient.create(
            IActivityApiService::class.java))

        val userViewModel: UserViewModel by viewModels {
            UserViewModelFactory(userRepository)
        }
        val activityViewModel: ActivityViewModel by viewModels {
            ActivityViewModelFactory(activityRepository)
        }

        setContent {
            MobileAppTheme {
                val navController = rememberNavController()

                AppNavGraph(
                    navController = navController,
                    userViewModel = userViewModel,
                    activityViewModel = activityViewModel
                )
            }
        }
    }
}