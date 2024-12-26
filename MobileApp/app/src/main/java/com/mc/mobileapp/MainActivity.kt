package com.mc.mobileapp

import AppNavGraph
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.navigation.compose.rememberNavController
import androidx.room.Room
import com.mc.mobileapp.ui.theme.MobileAppTheme
import kotlinx.coroutines.coroutineScope

class MainActivity : ComponentActivity() {
    companion object {
        lateinit var database: AppDatabase
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        database = Room.databaseBuilder(
            this.applicationContext,
            AppDatabase::class.java,
            "calaid_db"
        ).build()

        val userRepository = UserRepository(database.userDao())

        val userViewModel: UserViewModel by viewModels {
            UserViewModelFactory(userRepository)
        }
        setContent {
            MobileAppTheme {
                val navController = rememberNavController()

                AppNavGraph(
                    navController = navController,
                    userViewModel = userViewModel
                )
            }
        }
    }
}