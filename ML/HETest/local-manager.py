import redis, json
import threading
import base64
import numpy as np
import time
import pandas as pd
import joblib
import requests
from flask import Flask, request, jsonify
from process_data import process_data, getActivity
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from prometheus_flask_exporter import PrometheusMetrics
from concrete.ml.deployment import FHEModelClient, FHEModelDev, FHEModelServer

# model = joblib.load("lsvc_concrete_model.pkl")
# X_sample = np.load("sample_input.npy")
# model.compile(X_sample)

redis_client = redis.Redis(host="192.168.56.11", port=6379, decode_responses=True)


fhemodel_client = FHEModelClient("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model", key_dir="/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model")
serialized_evaluation_keys = fhemodel_client.get_serialized_evaluation_keys()

# Save the evaluation keys to file
with open("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model/serialized_evaluation_keys.ekl", "wb") as f:
    f.write(fhemodel_client.get_serialized_evaluation_keys())

#todo: change this such that it is 3 mins ago
user_id = "1"
key = f"user:user_{user_id}:raw_stream"
entries = redis_client.xrange(key, max="+", count=1000)
raw_data = []
for _, fields in entries:
    try:
        parsed = json.loads(fields["data"])
        raw_data.append(parsed)
    except json.JSONDecodeError:
        continue

df = pd.DataFrame(raw_data)

acc_data = df[df["sensorType"] == "accelerometer"].copy()
gyro_data = df[df["sensorType"] == "gyroscope"].copy()

df = process_data(acc_data, gyro_data)

decrypted_predictions = []
encrypted_batch = []

for i in range(df.shape[0]):
    clear_input = df.iloc[[i]].values  # shape: (1, n_features)
    encrypted_input = fhemodel_client.quantize_encrypt_serialize(clear_input)
    encrypted_batch.append(encrypted_input)



#worker
print(f"Received batch of size: {len(encrypted_batch)}")
#encrypted_batch = encrypted_batch[0]

results = []
with open("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model"+ "/serialized_evaluation_keys.ekl", "rb") as f:
    serialized_evaluation_keys = f.read()

fhemodel_server = FHEModelServer("/Users/mariaasoltanei/Desktop/FACULTATE/CERCETARE/HealthApp/ML/HETest/Model")  # path to compiled model directory
# for enc_b64 in encrypted_batch:
#     # print(f"Processing encrypted input: {enc_b64}")
#     print("-------------")
#     #encrypted_bytes = base64.b64decode(enc_b64)
#     # print(f"Decoded encrypted input: {encrypted_bytes}")
#     encrypted_result = fhemodel_server.run(enc_b64, serialized_evaluation_keys)

decrypted_predictions = []

for enc_b64 in encrypted_batch:
    #encrypted_bytes = base64.b64decode(enc_b64)
    encrypted_result = fhemodel_server.run(enc_b64, serialized_evaluation_keys)
    decrypted = fhemodel_client.deserialize_decrypt_dequantize(encrypted_result)[0]
    print(f"Decrypted prediction: {decrypted}")
    predicted_class = int(np.argmax(decrypted))
    print(f"Predicted class: {predicted_class}")
    label_classes = np.load("label_classes.npy")
    predicted_label = label_classes[predicted_class]
    print(f"Mapped activity: {predicted_label}")