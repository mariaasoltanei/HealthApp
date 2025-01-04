package com.clientmobile

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.room.Room
import com.clientmobile.User.UserRepository
import com.clientmobile.User.UserViewModel
import com.clientmobile.User.UserViewModelFactory
import com.clientmobile.ui.theme.ClientMobileTheme

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

        // Create the ViewModel using a factory
        val userViewModel: UserViewModel by viewModels {
            UserViewModelFactory(userRepository)
        }
        setContent {
            ClientMobileTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    // Use the RegisterScreen composable
                    RegisterScreen(
                        userViewModel = userViewModel,
                        onRegisterSuccess = {
                            // Handle success navigation or a success message here
                        }
                    )
                }
            }
        }
    }
}
