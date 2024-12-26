package com.mc.mobileapp.screens
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.gestures.Orientation
import androidx.compose.foundation.gestures.scrollable
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
import androidx.compose.runtime.getValue
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.ui.Modifier
import androidx.compose.ui.layout.ContentScale
import coil.compose.AsyncImage
import coil.compose.rememberImagePainter
import com.mc.mobileapp.ExerciseViewModel

@Composable
fun ActivityListScreen(
    onBack: () -> Unit,
    onActivityClick: (String) -> Unit,
    viewModel: ExerciseViewModel = viewModel()
) {
    val exerciseList by viewModel.exerciseList.collectAsStateWithLifecycle()
    val isLoading by viewModel.isLoading.collectAsStateWithLifecycle()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
            .background(color = MaterialTheme.colorScheme.background),
        verticalArrangement = Arrangement.SpaceBetween,
        horizontalAlignment = Alignment.Start
    ) {
        Column(
            modifier = Modifier.weight(1f)
        ) {
            Text(
                text = "Physical Activities",
                style = MaterialTheme.typography.titleLarge.copy(
                    fontSize = 24.sp,
                    fontWeight = FontWeight.Bold
                ),
                modifier = Modifier.padding(bottom = 16.dp)
            )

            if (isLoading) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = "Loading...",
                        style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp, color = Color.Gray)
                    )
                }
            } else {
                LazyColumn(
                    modifier = Modifier
                        .fillMaxSize()
                        .scrollable(
                            state = rememberScrollState(),
                            orientation = Orientation.Vertical
                        )
                ) {
                    items(exerciseList) { activity ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 8.dp)
                                .clickable { onActivityClick(activity.id) },
                            shape = RoundedCornerShape(8.dp),
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surface)
                        ) {
                            Row(
                                modifier = Modifier.padding(16.dp),
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                AsyncImage(
                                    model = activity.activityIcon,
                                    contentDescription = "Activity Icon",
                                    modifier = Modifier
                                        .size(40.dp)
                                        .padding(end = 16.dp),
                                    contentScale = ContentScale.Crop
                                )
                                Column {
                                    Text(
                                        text = "Activity: ${activity.activityName}",
                                        style = MaterialTheme.typography.bodyMedium.copy(fontSize = 18.sp)
                                    )
                                    Text(
                                        text = "Calories Burned: ${activity.caloriesBurned}",
                                        style = MaterialTheme.typography.bodySmall.copy(fontSize = 16.sp, color = Color.Gray)
                                    )
                                }
                            }
                        }
                    }
                }
            }
        }

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
}

