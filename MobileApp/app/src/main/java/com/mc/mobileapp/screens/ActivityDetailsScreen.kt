package com.mc.mobileapp.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.*
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.mc.mobileapp.ActivityViewModel
import com.mc.mobileapp.domains.ActivityData
import androidx.compose.runtime.getValue
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue

@Composable
fun ActivityDetailsScreen(
    activityId: String,
    viewModel: ActivityViewModel = viewModel(),
    onBack: () -> Unit
) {
    var activity by remember { mutableStateOf<ActivityData?>(null) }

    LaunchedEffect(activityId) {
        viewModel.getActivityById(activityId) { fetchedActivity ->
            activity = fetchedActivity
        }
    }

    activity?.let {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(24.dp)
                .background(color = MaterialTheme.colorScheme.background),
            verticalArrangement = Arrangement.Top,
            horizontalAlignment = Alignment.Start
        ) {
            Text(
                text = "Activity Details",
                style = MaterialTheme.typography.titleLarge.copy(
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold
                ),
                modifier = Modifier.padding(bottom = 16.dp)
            )

            Text(
                text = "Activity: ${it.activityName}",
                style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp),
                modifier = Modifier.padding(bottom = 8.dp)
            )

            Text(
                text = "Calories Burned: ${it.caloriesBurned}",
                style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp),
                modifier = Modifier.padding(bottom = 8.dp)
            )

            Text(
                text = "Duration: ${it.duration}",
                style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp),
                modifier = Modifier.padding(bottom = 8.dp)
            )

            Text(
                text = "Average Heart Rate: ${it.averageHeartRate} bpm",
                style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp),
                modifier = Modifier.padding(bottom = 8.dp)
            )

            Text(
                text = "Steps Taken: ${it.stepsTaken}",
                style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp),
                modifier = Modifier.padding(bottom = 8.dp)
            )

            Text(
                text = "Date: ${it.activityDateTime}",
                style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp),
                modifier = Modifier.padding(bottom = 8.dp)
            )

            Text(
                text = "Notes: ${it.notes}",
                style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp),
                modifier = Modifier.padding(bottom = 8.dp)
            )

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                onClick = onBack,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(vertical = 8.dp),
                shape = RoundedCornerShape(8.dp),
                colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
            ) {
                Text(
                    text = "Back",
                    style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp, color = Color.White)
                )
            }
        }
    } ?: Box(
        modifier = Modifier.fillMaxSize(),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = "Loading Activity Details...",
            style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp, color = Color.Gray)
        )
    }
}