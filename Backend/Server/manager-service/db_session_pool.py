from iotdb.SessionPool import SessionPool, PoolConfig

IOTDB_HOST = "192.168.56.15"  
IOTDB_PORT = 6667  
USERNAME = "root"   
PASSWORD = "root"

max_pool_size = 10
wait_timeout_in_ms = 3000

def get_session_pool():
    pool_config = PoolConfig(host=IOTDB_HOST,port=IOTDB_PORT, user_name=USERNAME,
                         password=PASSWORD)
    session_pool = SessionPool(pool_config, max_pool_size, wait_timeout_in_ms)

    return session_pool

