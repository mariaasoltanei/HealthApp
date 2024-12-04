import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.mc.mobileapp.UserViewModel
import com.mc.mobileapp.screens.LandingScreen
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
                    navController.navigate("landing")
                },
                onBackClick = { navController.popBackStack() } // Navigate back to welcome
            )
        }

        // Register Screen
        composable("register") {
            RegisterScreen(
                userViewModel = userViewModel,
                onRegisterSuccess = {
                    navController.navigate("landing")
                },

                onBackClick = { navController.popBackStack() } // Navigate back to welcome
            )
        }

        //Landing Screen
        composable("landing") {
            LandingScreen(
                onSucessful = {
                    navController.navigate("welcome") {
                        popUpTo("welcome") { inclusive = true }
                    }
                }
            )
        }
    }
}
