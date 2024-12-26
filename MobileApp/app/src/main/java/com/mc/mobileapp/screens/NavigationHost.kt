import androidx.compose.runtime.Composable
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.mc.mobileapp.UserViewModel
import com.mc.mobileapp.screens.ActivityDetailsScreen
import com.mc.mobileapp.screens.ActivityListScreen
import com.mc.mobileapp.screens.LandingScreen
import com.mc.mobileapp.screens.LoginScreen
import com.mc.mobileapp.screens.RegisterScreen
import com.mc.mobileapp.screens.WelcomeScreen
import androidx.navigation.NavType
import androidx.navigation.navArgument
import com.mc.mobileapp.ExerciseViewModel

@Composable
fun AppNavGraph(navController: NavHostController, userViewModel: UserViewModel, exerciseViewModel: ExerciseViewModel) {
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
                onLogout = {
                    navController.navigate("welcome") {
                        popUpTo("welcome") { inclusive = true }
                    }
                },
                onViewActivities = { navController.navigate("activities") }
            )
        }
        // Activities Screen
        composable("activities") {
            ActivityListScreen(
                onBack = { navController.popBackStack() },
                onActivityClick = { activityId ->
                    navController.navigate("activityDetails/$activityId")
                },
                viewModel = exerciseViewModel
            )
        }

        // Activity Details Screen
        composable(
            route = "activityDetails/{activityId}",
            arguments = listOf(navArgument("activityId") { type = NavType.StringType })
        ) { backStackEntry ->
            val activityId = backStackEntry.arguments?.getString("activityId") ?: ""

            ActivityDetailsScreen(
                activityId = activityId,
                viewModel = exerciseViewModel,
                onBack = { navController.popBackStack() }
            )
        }
    }
}
