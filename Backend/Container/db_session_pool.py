from iotdb.SessionPool import SessionPool, PoolConfig
import atexit

IOTDB_HOST = "192.168.0.106"  
IOTDB_PORT = 6667  
USERNAME = "root"   
PASSWORD = "root"
pool_config = PoolConfig(host=IOTDB_HOST,port=IOTDB_PORT, user_name=USERNAME,
                         password=PASSWORD, fetch_size=1024,
                         time_zone="UTC+8", max_retry=3)
max_pool_size = 5
wait_timeout_in_ms = 3000

session_pool = SessionPool(pool_config, max_pool_size, wait_timeout_in_ms)
atexit.register(session_pool.close)