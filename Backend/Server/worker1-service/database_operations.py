from db_session_pool import session_pool
import pandas as pd
from datetime import datetime, timedelta

def pull_last_5_minutes_data(user_id):
    try:
        session = session_pool.get_session()

        now = datetime.utcnow()
        
        #test_Time= datetime(2025, 4, 29, 12, 30, 0)  # Replace with your test time
        db_time = now + timedelta(hours=3)
        five_minutes_ago = db_time - timedelta(minutes=5)
        print(f"Five minutes ago: {five_minutes_ago}")
        now_millis = int(db_time.timestamp() * 1000)
        print(f"Current time in milliseconds: {now_millis}")
        past_millis = int(five_minutes_ago.timestamp() * 1000)

        accelerometer_path = f"root.users.{user_id}.accelerometer"
        gyroscope_path = f"root.users.{user_id}.gyroscope"

        sql_query_acc = f"""
        SELECT * FROM {accelerometer_path}
        WHERE time >= {past_millis} and time <= {now_millis}
        """

        sql_query_gyro = f"""
        SELECT * FROM {gyroscope_path}
        WHERE time >= {past_millis} and time <= {now_millis}
        """

        acc_result = session.execute_query_statement(sql_query_acc)
        acc_df = acc_result.todf()

        gyro_result = session.execute_query_statement(sql_query_gyro)
        gyro_df = gyro_result.todf()

        return acc_df, gyro_df

    except Exception as e:
        print(f"❌ Error pulling data from IoTDB: {e}")
        return None, None
    
    finally:
        if session:
            try:
                session.close()
                print("✅ IoTDB session closed properly.")
            except Exception as e:
                print(f"⚠️ Error closing session: {e}")