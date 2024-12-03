import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import java.text.SimpleDateFormat
import java.util.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DatePickerDialog(
    onDismissRequest: () -> Unit,
    onConfirm: (String) -> Unit
) {

    val datePickerState = rememberDatePickerState()
    val formatter = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault())

    DatePickerDialog(
        onDismissRequest = onDismissRequest,
        confirmButton = {
            TextButton(onClick = {
                val selectedDate = datePickerState.selectedDateMillis?.let { millis ->
                    val calendar = Calendar.getInstance().apply { timeInMillis = millis }
                    formatter.format(calendar.time)
                } ?: "Invalid date"

                onConfirm(selectedDate)
            }) {
                Text("OK")
            }
        },
        dismissButton = {
            TextButton(onClick = onDismissRequest) {
                Text("Cancel")
            }
        }
    ) {
        DatePicker(state = datePickerState)
    }
}
