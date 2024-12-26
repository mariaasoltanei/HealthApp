import androidx.compose.runtime.Composable
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavHostController
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.navArgument
import com.mc.mobileapp.ExerciseRepository
import com.mc.mobileapp.ExerciseViewModel
import com.mc.mobileapp.ExerciseViewModelFactory
import com.mc.mobileapp.MainActivity
import com.mc.mobileapp.UserViewModel
import com.mc.mobileapp.retrofit.IExerciseApiService
import com.mc.mobileapp.retrofit.RetrofitClient
import com.mc.mobileapp.screens.ActivityDetailsScreen
import com.mc.mobileapp.screens.ActivityListScreen
import com.mc.mobileapp.screens.LandingScreen
import com.mc.mobileapp.screens.LoginScreen
import com.mc.mobileapp.screens.RegisterScreen
import com.mc.mobileapp.screens.WelcomeScreen

@Composable
fun AppNavGraph(navController: NavHostController, userViewModel: UserViewModel) {
    val apiService: IExerciseApiService = RetrofitClient.create(IExerciseApiService::class.java)
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
        composable("activities") {
            val repository = ExerciseRepository(MainActivity.database.exerciseDataDao(), apiService)
            val viewModel: ExerciseViewModel =
                viewModel(factory = ExerciseViewModelFactory(repository))
            ActivityListScreen(
                onBack = { navController.popBackStack() },
                onActivityClick = { exerciseId -> navController.navigate("activity_details/$exerciseId") },
                viewModel = viewModel
            )
        }
        composable(
            route = "activity_details/{exerciseId}",
            arguments = listOf(navArgument("exerciseId") { type = NavType.IntType })
        ) { backStackEntry ->
            val exerciseId = backStackEntry.arguments?.getInt("exerciseId") ?: 0
            val repository = ExerciseRepository(MainActivity.database.exerciseDataDao(), apiService)
            val viewModel: ExerciseViewModel =
                viewModel(factory = ExerciseViewModelFactory(repository))
            ActivityDetailsScreen(
                exerciseId = exerciseId,
                viewModel = viewModel,
                onBack = { navController.popBackStack() }
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
    }
}
