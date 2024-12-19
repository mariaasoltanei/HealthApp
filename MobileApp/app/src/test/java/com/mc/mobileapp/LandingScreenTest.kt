import android.content.Context
import android.content.Intent
import androidx.compose.ui.test.junit4.createComposeRule
import androidx.compose.ui.test.*
import androidx.test.ext.junit.runners.AndroidJUnit4
import com.mc.mobileapp.SensorService
import com.mc.mobileapp.screens.LandingScreen
import org.junit.After
import org.junit.Before
import org.junit.Rule
import org.junit.Test
import org.junit.runner.RunWith
import org.mockito.Mockito.*

/**
 * Unit tests for LandingScreen
 */
@RunWith(AndroidJUnit4::class)
class LandingScreenTest {

    @get:Rule
    val composeTestRule = createComposeRule()

    private lateinit var mockContext: Context

    @Before
    fun setup() {
        mockContext = mock(Context::class.java) // Mock the Android context
    }

    @After
    fun teardown() {
        // Reset all interactions with the mock to avoid side effects
        reset(mockContext)
    }

    /**
     * Test that the SensorService is started when the LandingScreen is displayed.
     */
    @Test
    fun `when LandingScreen is loaded, SensorService should be started`() {
        // Act
        composeTestRule.setContent {
            LandingScreen(onLogout = {})
        }

        // Verify that startService was called once
        verify(mockContext, times(1)).startService(argThat { intent ->
            intent.component?.className == SensorService::class.java.name
        })
    }

    /**
     * Test that the SensorService is stopped when the Log Out button is clicked.
     */
    @Test
    fun `when Log Out button is clicked, SensorService should be stopped`() {
        // Arrange
        composeTestRule.setContent {
            LandingScreen(onLogout = {})
        }

        // Act: Simulate a button click for "Log Out"
        composeTestRule.onNodeWithText("Log Out").performClick()

        // Verify that stopService was called once
        verify(mockContext, times(1)).stopService(argThat { intent ->
            intent.component?.className == SensorService::class.java.name
        })
    }

    /**
     * Test that the Log Out button is displayed on the LandingScreen.
     */
    @Test
    fun `when LandingScreen is loaded, Log Out button is visible`() {
        // Act
        composeTestRule.setContent {
            LandingScreen(onLogout = {})
        }

        // Assert that the Log Out button exists
        composeTestRule.onNodeWithText("Log Out").assertExists()
    }
}
