from iotdb.SessionPool import SessionPool, PoolConfig

IOTDB_HOST = "192.168.56.15"
IOTDB_PORT = 6667
USERNAME = "root"
PASSWORD = "root"

max_pool_size = 15
wait_timeout_in_ms = 3000

pool_config = PoolConfig(host=IOTDB_HOST,port=IOTDB_PORT, user_name=USERNAME,password=PASSWORD)
session_pool = SessionPool(pool_config, max_pool_size, wait_timeout_in_ms)

def get_session_pool():
    return session_pool
