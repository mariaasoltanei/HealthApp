from locust import HttpUser, task, between
import random
import time


class SensorDataUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def test_valid_sensor_data(self):
        """Simulate valid sensor data upload."""
        sensor_data = self.generate_sensor_data_batch()
        headers = {"X-API-Key": "IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7"}
        response = self.client.post("/upload", json=sensor_data, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.json()}")

    @task
    def test_invalid_sensor_type(self):
        """Simulate an invalid sensor type."""
        sensor_data = self.generate_sensor_data_batch()
        for data in sensor_data:
            data["sensorType"] = "invalid_sensor"  # Overwrite with invalid type
        headers = {"X-API-Key": "IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7"}
        response = self.client.post("/upload", json=sensor_data, headers=headers)
        if response.status_code != 400:
            print(f"Expected 400 but got {response.status_code}: {response.json()}")

    @task
    def test_abnormal_g_force(self):
        """Simulate abnormal g-force."""
        sensor_data = self.generate_sensor_data_batch()
        for data in sensor_data:
            data["x"], data["y"], data["z"] = 500, 500, 500  # Overwrite with high values
        headers = {"X-API-Key": "IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7"}
        response = self.client.post("/upload", json=sensor_data, headers=headers)
        if "Abnormal G-force detected" not in response.text:
            print(f"{response.json()}")

    @task
    def test_abnormal_gyroscope_rotation(self):
        """Simulate abnormal gyroscope rotation."""
        sensor_data = self.generate_sensor_data_batch()
        for data in sensor_data:
            data["x"], data["y"], data["z"] = 300, 300, 300  # Overwrite with high rotation values
        headers = {"X-API-Key": "IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7"}
        response = self.client.post("/upload", json=sensor_data, headers=headers)
        if "Abnormal gyroscope rotation detected" not in response.text:
            print(f"{response.json()}")

    @task
    def test_banned_user(self):
        """Simulate a banned user."""
        sensor_data = self.generate_sensor_data_batch()
        for data in sensor_data:
            data["userTrustScore"] = 0  # Simulate banned user
        headers = {"X-API-Key": "IGtluHxC6SSVQJleAnwvrq0CM5ZuxdXdXfeqojdA3U7"}
        response = self.client.post("/upload", json=sensor_data, headers=headers)
        if response.status_code != 403 or "User banned" not in response.text:
            print(f"Unexpected response: {response.status_code} {response.json()}")


    def generate_sensor_data_error(self, user_id=None, sensorType=None):
        """Generate realistic sensor data."""
        return {
            "userId": user_id or random.randint(1, 100),
            "userTrustScore": 100,
            "x": round(random.uniform(-10.0, 10.0), 2),
            "y": round(random.uniform(-10.0, 10.0), 2),
            "z": round(random.uniform(-10.0, 10.0), 2),
            "sensorType": sensorType or random.choice(["accelerometer", "gyroscope"]),
            "timestamp": int(time.time() * 1000),
        }

    def generate_sensor_data_batch(self):
        """Generate a batch of 150 sensor data entries with consecutive timestamps."""
        base_timestamp = int(time.time() * 1000)
        sensor_data_list = []

        for i in range(150):
            sensor_data = {
                "userId": random.randint(1, 100),
                "userTrustScore": 100,
                "x": round(random.uniform(-10.0, 10.0), 2),
                "y": round(random.uniform(-10.0, 10.0), 2),
                "z": round(random.uniform(-10.0, 10.0), 2),
                "sensorType": random.choice(["accelerometer", "gyroscope"]),
                "timestamp": base_timestamp + i * 66
            }
            sensor_data_list.append(sensor_data)

        return sensor_data_list