def calculate_batch_magnitude_sum(data):
    return sum((entry['x']**2 + entry['y']**2 + entry['z']**2)**0.5 for entry in data if entry['sensorType'] == 'accelerometer')

def check_gyroscope_rotation(data):
    max_rotation = max(abs(entry['x']) for entry in data if entry['sensorType'] == 'gyroscope')
    return max_rotation