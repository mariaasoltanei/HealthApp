package com.mc.mobileapp

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.mc.mobileapp.daos.ActivityDataDao
import com.mc.mobileapp.domains.ActivityData
import com.mc.mobileapp.retrofit.IActivityApiService
import com.mc.mobileapp.retrofit.RetrofitClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ActivityViewModel(private val repository: ActivityRepository) : ViewModel() {
    private val _activityList = MutableStateFlow<List<ActivityData>>(emptyList())
    val activityList: StateFlow<List<ActivityData>> get() = _activityList

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> get() = _isLoading

    init {
        fetchActivities()
    }

    private fun fetchActivities() {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val activities = repository.getAllActivities()
                _activityList.value = activities
            } catch (e: Exception) {
                Log.e("ActivityViewModel", "Error fetching activities: ${e.message}")
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun getActivityById(id: String, onSuccess: (ActivityData?) -> Unit) {
        viewModelScope.launch(Dispatchers.IO) {
            val activity = repository.getActivityById(id)
            onSuccess(activity)
        }
    }
}

// ViewModel Factory
class ActivityViewModelFactory(private val repository: ActivityRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(ActivityViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return ActivityViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}