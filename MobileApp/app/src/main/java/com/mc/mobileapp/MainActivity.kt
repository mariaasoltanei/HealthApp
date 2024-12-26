package com.mc.mobileapp

import AppNavGraph
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.navigation.compose.rememberNavController
import androidx.room.Room
import com.mc.mobileapp.retrofit.IExerciseApiService
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
            "health_app_database"
        )
            .build()


        val userRepository = UserRepository(database.userDao())
        val exerciseRepository = ExerciseRepository(database.exerciseDataDao(), apiService = RetrofitClient.create(
            IExerciseApiService::class.java))

        val userViewModel: UserViewModel by viewModels {
            UserViewModelFactory(userRepository)
        }
        val exerciseViewModel: ExerciseViewModel by viewModels {
            ExerciseViewModelFactory(exerciseRepository)
        }

        setContent {
            MobileAppTheme {
                val navController = rememberNavController()

                AppNavGraph(
                    navController = navController,
                    userViewModel = userViewModel,
                    exerciseViewModel = exerciseViewModel
                )
            }
        }
    }
}