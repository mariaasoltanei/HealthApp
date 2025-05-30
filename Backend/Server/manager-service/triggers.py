import os
import time
import requests

WORKER1_SERVICE = os.getenv("WORKER1_SERVICE", "worker1")
WORKER2_SERVICE = os.getenv("WORKER2_SERVICE", "worker2")
WORKER3_SERVICE = os.getenv("WORKER3_SERVICE", "worker3")

def periodic_trigger_worker3():
    while True:
        try:
            print("Triggering Worker3 for FHE inference...")
            user_id= "user_1"
            url3 = f"http://{WORKER3_SERVICE}:6000/trigger/{user_id}"
            try:
                res = requests.post(url3, timeout=5)
                if res.ok:
                    print(f"Triggered Worker3 for user: {user_id}")
                else:
                    print(f"Worker3 failed to respond for user: {user_id} — Status: {res.status_code}")
            except Exception as req_error:
                print(f"Error contacting Worker3 for user {user_id}: {req_error}")

        except Exception as e:
            print(f"Unexpected error in periodic_trigger_worker3: {e}")

        time.sleep(30)  # todo: every 3 minutes

def vote(pred1, pred2):
    if pred1["prediction"] == pred2["prediction"]:
        return pred1["prediction"]
    return pred1["prediction"] if pred1["confidence"] > pred2["confidence"] else pred2["prediction"]

def periodic_trigger_workers():
    while True:
        try:
            print("Triggering workers...")
            user_id = "user_1"
            url1 = f"http://{WORKER1_SERVICE}:6000/trigger/{user_id}"
            url2 = f"http://{WORKER2_SERVICE}:6000/trigger/{user_id}"

            max_retries = 3
            delay = 2

            pred1 = pred2 = None

            for attempt in range(max_retries):
                if not pred1:
                    res1 = requests.post(url1, timeout=5)
                    if res1.ok:
                        p1 = res1.json()
                        if "prediction" in p1 and "confidence" in p1:
                            pred1 = p1

                if not pred2:
                    res2 = requests.post(url2, timeout=5)
                    if res2.ok:
                        p2 = res2.json()
                        if "prediction" in p2 and "confidence" in p2:
                            pred2 = p2

                if pred1 and pred2:
                    break  # both predictions received

                time.sleep(delay)  # wait before retrying

            if pred1 and pred2:
                final = vote(pred1, pred2)
                print(f"Final activity for {user_id}: {final}")
            else:
                print(f"Could not collect both predictions after retries for {user_id}")

        except Exception as e:
            print(f"Error triggering workers: {e}")

        time.sleep(30)  # or 300 for 5 minutes