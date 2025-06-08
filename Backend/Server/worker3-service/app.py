import pandas as pd
import joblib
import json
import time
import base64
import numpy as np
import tenseal as ts
from flask import Flask, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
model = joblib.load("model.pkl")

@app.route('/trigger/<user_id>', methods=['POST'])
def trigger(user_id):
    try:
        print(f"Triggered worker3: {user_id}")
        data = request.get_json()
        encrypted_b64 = data.get("encrypted_features")
        context_b64 = data.get("context")

        # Decode base64 to bytes
        encrypted_bytes = base64.b64decode(encrypted_b64)
        context_bytes = base64.b64decode(context_b64)

        # Load context and encrypted vector
        context = ts.context_from(context_bytes)
        encrypted_vector = ts.ckks_vector_from(context, encrypted_bytes)

        weights = model.coef_
        bias = model.intercept_

        # Run inference
        logits = [encrypted_vector.dot(w) + b for w, b in zip(weights, bias)]
        encrypted_logits_b64 = [base64.b64encode(logit.serialize()).decode("utf-8") for logit in logits]
        return jsonify({"encrypted_logits": encrypted_logits_b64}), 200

    except Exception as e:
        print(f"Error in /trigger: {e}")
        return jsonify({"error": str(e)}), 500

# @app.route('/trigger/<user_id>', methods=['POST'])
# def trigger(user_id):
#     try:
#         print(f"Triggeed worker3: {user_id}")
#         data = request.get_json()
#         encrypted_b64 = data.get("encrypted_features")
#         context_b64 = data.get("context")

#         print(f"Encrypted payload length: {len(encrypted_b64)}")
#         print(f"Context payload length: {len(context_b64)}")
#         return jsonify({"status": "success"}), 200

#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=6000)
