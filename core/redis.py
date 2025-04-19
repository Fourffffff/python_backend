import redis

# 初始化 Redis 连接
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
