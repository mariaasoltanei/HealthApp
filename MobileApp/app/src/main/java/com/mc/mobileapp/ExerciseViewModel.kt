package com.mc.mobileapp

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.mc.mobileapp.domains.ExerciseData
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ExerciseViewModel(private val repository: ExerciseRepository) : ViewModel() {
    private val _exerciseList = MutableStateFlow<List<ExerciseData>>(emptyList())
    val exerciseList: StateFlow<List<ExerciseData>> get() = _exerciseList

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> get() = _isLoading

    init {
        fetchActivities()
    }

    private fun fetchActivities() {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                val activities = repository.getAllExercises()
                _exerciseList.value = activities
            } catch (e: Exception) {
                Log.e("ExerciseViewModel", "Error fetching activities: ${e.message}")
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun getExerciseById(id: String, onSuccess: (ExerciseData?) -> Unit) {
        viewModelScope.launch(Dispatchers.IO) {
            val exercise = repository.getExerciseById(id)
            onSuccess(exercise)
        }
    }
}

class ExerciseViewModelFactory(private val repository: ExerciseRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(ExerciseViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return ExerciseViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}