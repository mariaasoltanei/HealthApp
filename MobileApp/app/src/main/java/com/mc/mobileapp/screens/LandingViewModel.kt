

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.mc.mobileapp.daos.UserDao
import com.mc.mobileapp.domains.UserHealthData
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.launch

class LandingViewModel(
    private val userDao: UserDao,
    private val userId: Int
) : ViewModel() {

    private val _userHealthData = MutableStateFlow<UserHealthData?>(null)
    val userHealthData: StateFlow<UserHealthData?> = _userHealthData.asStateFlow()

    init {
        loadUserHealthData()
    }

    private fun loadUserHealthData() {
        viewModelScope.launch {
            userDao.getUserById(userId)
                .map { user ->
                    user?.let {
                        UserHealthData(
                            gender = it.gender,
                            height = it.height,
                            weight = it.weight,
                            birthDate = it.birthDate,
                            activityMultiplier = it.activityMultiplier
                        )
                    }
                }
                .collect { userHealthData ->
                    _userHealthData.value = userHealthData
                }
        }
    }
}