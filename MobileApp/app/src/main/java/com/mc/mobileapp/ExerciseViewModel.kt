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

    fun fetchExercises() {
        viewModelScope.launch(Dispatchers.IO) {
            _isLoading.value = true
            try {
                val exercises = repository.getAllExercises()
                _exerciseList.value = exercises
            } catch (e: Exception) {
                Log.e("ExerciseViewModel", "Error fetching exercises: ${e.message}")
            } finally {
                _isLoading.value = false
            }
        }
    }

    fun getExerciseById(id: String, onSuccess: (ExerciseData?) -> Unit) {
        viewModelScope.launch(Dispatchers.IO) {
            val exercise = repository.getExerciseById(Integer.parseInt(id))
            onSuccess(exercise)
        }
    }
}


class ExerciseViewModelFactory(private val repository: ExerciseRepository) :
    ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(ExerciseViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return ExerciseViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
