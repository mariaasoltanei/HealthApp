from db_session_pool import get_session_pool
import pandas as pd
from datetime import datetime, timedelta

session_pool = get_session_pool()

def pull_last_5_minutes_data(user_id):
    session = None
    try:
        session = session_pool.get_session()
        session.open()

        now = datetime.utcnow()
        five_minutes_ago = now - timedelta(minutes=5)

        now_millis = int(now.timestamp() * 1000)
        past_millis = int(five_minutes_ago.timestamp() * 1000)

        accelerometer_path = f"root.he.users.{user_id}.accelerometer"
        gyroscope_path = f"root.he.users.{user_id}.gyroscope"

        # Pull accelerometer
        sql_query_acc = f"""
        SELECT * FROM {accelerometer_path}
        WHERE time >= {past_millis} and time <= {now_millis}
        """

        # Pull gyroscope
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
                session_pool.put_back(session)
                print("✅ IoTDB session closed properly.")
            except Exception as e:
                print(f"⚠️ Error closing session: {e}")