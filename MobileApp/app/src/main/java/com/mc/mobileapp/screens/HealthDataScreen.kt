package com.mc.mobileapp.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import com.mc.mobileapp.components.DatePickerField
import com.mc.mobileapp.components.Dropdown

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HealthDataScreen(
    birthDate: String,
    gender: String,
    height: String,
    weight: String,
    activityMultiplier: String,
    onBirthDateChange: (String) -> Unit,
    onGenderChange: (String) -> Unit,
    onHeightChange: (String) -> Unit,
    onWeightChange: (String) -> Unit,
    onActivityMultiplierChange: (String) -> Unit,
    onRegister: () -> Unit,
    onBack: () -> Unit,
    errorMessage: String
) {
    val activityLevels = mapOf(
        "Sedentary" to 1.2f,
        "Active" to 1.55f,
        "Very Active" to 1.9f
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text("Health Information", style = MaterialTheme.typography.titleMedium)

        DatePickerField(
            label = "Birth Date",
            selectedDate = birthDate,
            onDateChange = onBirthDateChange,
            modifier = Modifier.fillMaxWidth()
        )
        // Gender Dropdown
        Dropdown(
            dropdownItems = mapOf("Male" to 0f, "Female" to 0f),
            label = "Gender",
            selectedItem = gender,
            onSelectedItemChange = onGenderChange,
            modifier = Modifier.fillMaxWidth()
        )

        // Activity Multiplier Dropdown
        Dropdown(
            dropdownItems = activityLevels,
            label = "Activity Multiplier",
            selectedItem = activityMultiplier,
            onSelectedItemChange = { selectedLabel ->
                val numericValue = activityLevels[selectedLabel] ?: 1.0f
                onActivityMultiplierChange(numericValue.toString())
            },
            modifier = Modifier.fillMaxWidth()
        )
        TextField(
            value = height,
            onValueChange = onHeightChange,
            label = { Text("Height (cm)") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth()
        )
        TextField(
            value = weight,
            onValueChange = onWeightChange,
            label = { Text("Weight (kg)") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth()
        )

        if (errorMessage.isNotBlank()) {
            Text(text = errorMessage, color = MaterialTheme.colorScheme.error)
        }

        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            Button(onClick = onBack) { Text("Back") }
            Button(onClick = onRegister) { Text("Register") }
        }
    }
}

