import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.mc.mobileapp.UserViewModel
import com.mc.mobileapp.screens.LoginScreen
import com.mc.mobileapp.screens.RegisterScreen
import com.mc.mobileapp.screens.WelcomeScreen

@Composable
fun AppNavGraph(navController: NavHostController, userViewModel: UserViewModel) {
    NavHost(navController = navController, startDestination = "welcome") {
        // Welcome Screen
        composable("welcome") {
            WelcomeScreen(
                onLoginClick = { navController.navigate("login") },
                onRegisterClick = { navController.navigate("register") }
            )
        }

        // Login Screen
        composable("login") {
            LoginScreen(
                userViewModel = userViewModel,
                onLoginSuccess = {
                    // Handle successful login (e.g., navigate to home screen or show toast)
                },
                onBackClick = { navController.popBackStack() } // Navigate back to welcome
            )
        }

        // Register Screen
        composable("register") {
            RegisterScreen(
                userViewModel = userViewModel,
                onRegisterSuccess = {
                    navController.navigate("login") { popUpTo("welcome") }
                },

                onBackClick = { navController.popBackStack() } // Navigate back to welcome
            )
        }
    }
}
