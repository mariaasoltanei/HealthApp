import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.test.*
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.mockito.kotlin.*
import com.mc.mobileapp.domains.User

import com.mc.mobileapp.UserRepository
import com.mc.mobileapp.UserViewModel
import com.mc.mobileapp.daos.UserDao

@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {

    @get:Rule
    val instantExecutorRule = InstantTaskExecutorRule()

    private lateinit var userDao: UserDao
    private lateinit var userRepository: UserRepository
    private lateinit var userViewModel: UserViewModel

    private val testDispatcher = UnconfinedTestDispatcher()

    @Before
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        userDao = mock()
        userRepository = UserRepository(userDao)
        userViewModel = UserViewModel(userRepository)
    }

    @After
    fun tearDown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `registerUser inserts user successfully and triggers onSuccess`() = runTest {
        // Arrange
        val user = User(
            firstName = "John",
            lastName = "Doe",
            email = "john.doe@example.com",
            password = "password123",
            birthDate = "1990-01-01",
            height = 180f,
            weight = 75f,
            gender = "Male",
            activityMultiplier = 1.2f
        )
        val onSuccess: () -> Unit = mock()
        val onError: (String) -> Unit = mock()

        // Act
        userViewModel.registerUser(user, onSuccess = onSuccess, onError = onError)
        advanceUntilIdle()

        // Assert
        verify(userDao).insertUser(user)
        verify(onSuccess).invoke()
        verify(onError, never()).invoke(any())
    }

    @Test
    fun `registerUser handles error correctly and triggers onError`() = runTest {
        // Arrange
        val user = User(
            firstName = "Jane",
            lastName = "Doe",
            email = "jane.doe@example.com",
            password = "password123",
            birthDate = "1990-01-01",
            height = 170f,
            weight = 60f,
            gender = "Female",
            activityMultiplier = 1.1f
        )
        val onSuccess: () -> Unit = mock()
        val onError: (String) -> Unit = mock()

        // Simulate an exception when inserting a user
        whenever(userDao.insertUser(user)).thenThrow(RuntimeException("Database error"))

        // Act
        userViewModel.registerUser(user, onSuccess = onSuccess, onError = onError)
        advanceUntilIdle()

        // Assert
        verify(userDao).insertUser(user)
        verify(onError).invoke("Database error")
        verify(onSuccess, never()).invoke()
    }

    @Test
    fun `loginUser succeeds with correct email and password`() = runTest {
        // Arrange
        val user = User(
            firstName = "John",
            lastName = "Doe",
            email = "john.doe@example.com",
            password = "password123",
            birthDate = "1990-01-01",
            height = 180f,
            weight = 75f,
            gender = "Male",
            activityMultiplier = 1.2f
        )
        val onSuccess: (User) -> Unit = mock()
        val onError: (String) -> Unit = mock()

        whenever(userDao.findUserEmailPassword(user.email, user.password)).thenReturn(user)

        // Act
        userViewModel.loginUser(user.email, user.password, onSuccess = onSuccess, onError = onError)
        advanceUntilIdle()

        // Assert
        verify(userDao).findUserEmailPassword(user.email, user.password)
        verify(onSuccess).invoke(user)
        verify(onError, never()).invoke(any())
    }

    @Test
    fun `loginUser fails with incorrect email or password`() = runTest {
        // Arrange
        val onSuccess: (User) -> Unit = mock()
        val onError: (String) -> Unit = mock()

        whenever(userDao.findUserEmailPassword("wrong@example.com", "wrongpassword")).thenReturn(null)

        // Act
        userViewModel.loginUser("wrong@example.com", "wrongpassword", onSuccess = onSuccess, onError = onError)
        advanceUntilIdle()

        // Assert
        verify(userDao).findUserEmailPassword("wrong@example.com", "wrongpassword")
        verify(onError).invoke("Invalid email or password.")
        verify(onSuccess, never()).invoke(any())
    }

    @Test
    fun `loginUser handles database error`() = runTest {
        // Arrange
        val onSuccess: (User) -> Unit = mock()
        val onError: (String) -> Unit = mock()

        whenever(userDao.findUserEmailPassword(any(), any())).thenThrow(RuntimeException("Database error"))

        // Act
        userViewModel.loginUser("test@example.com", "password123", onSuccess = onSuccess, onError = onError)
        advanceUntilIdle()

        // Assert
        verify(userDao).findUserEmailPassword("test@example.com", "password123")
        verify(onError).invoke("Database error")
        verify(onSuccess, never()).invoke(any())
    }
}
