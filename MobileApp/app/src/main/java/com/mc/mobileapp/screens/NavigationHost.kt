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
import com.mc.mobileapp.UserRepository
import com.mc.mobileapp.UserViewModel
import com.mc.mobileapp.retrofit.IExerciseApiService
import com.mc.mobileapp.retrofit.RetrofitClient
import com.mc.mobileapp.screens.ActivityDetailsScreen
import com.mc.mobileapp.screens.ActivityListScreen
import com.mc.mobileapp.screens.LandingScreen
import com.mc.mobileapp.screens.LandingViewModelFactory
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
                onLoginSuccess = { user ->
                    user.let {
                        navController.navigate("landing/${it.id}")
                    }
                },
                onBackClick = { navController.popBackStack() }
            )
        }

        // Register Screen
        composable("register") {
            RegisterScreen(
                userViewModel = userViewModel,
                onRegisterSuccess = { user ->
                    user.let {
                        navController.navigate("landing/${it.id}")
                    }
                },
                onBackClick = { navController.popBackStack() } // Navigate back to welcome
            )
        }

        //Activities Screen
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

        //Activity Details Screen
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
        // Landing Screen
        composable(
            route = "landing/{id}",
            arguments = listOf(navArgument("id") { type = NavType.IntType })
        ) { backStackEntry ->
            val id = backStackEntry.arguments?.getInt("id") ?: 0
            val dao = MainActivity.database.userDao()
            val landingViewModel: LandingViewModel =
                viewModel(factory = LandingViewModelFactory(dao, id))

            LandingScreen(
                viewModel = landingViewModel,
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
