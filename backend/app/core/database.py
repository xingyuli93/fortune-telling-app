import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取数据库连接信息
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("请设置 DATABASE_URL 环境变量")

# 创建一个数据库连接池
# 最小连接数: 1, 最大连接数: 10
connection_pool = SimpleConnectionPool(1, 10, dsn=DATABASE_URL)

def get_db_connection():
    """从连接池中获取一个数据库连接"""
    return connection_pool.getconn()

def release_db_connection(conn):
    """将数据库连接释放回连接池"""
    connection_pool.putconn(conn)
