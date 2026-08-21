# import redis
import redis
import json

# connect to redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# simple string keys and value usage
r.set("name", "Muhtasham")
r.set("age", 21)
r.incr("age")
r.incr("age")
r.incrby("age", 2)

print(r.get("name"))
print(r.get("age"))

# hash usage
r.hset("user:1", mapping={"name":"Muhtasham", "age":21, "city":"Lahore", "role":"dev"})
print(r.hget("user:1", "name"))
print(r.hget("user:1", "age"))
r.hincrby("user:1", "age", 2)
print(r.hgetall("user:1"))
print(r.hexists("user:1", "name"))

# list usage
r.lpush("notifications:user:1", "New comment on your post")
r.lpush("notifications:user:1", "Ali started following you")
r.lpush("notifications:user:1", "Your post got 100 likes")

r.rpop("notifications:user:1")
print(r.lrange("notifications:user:1", 0, -1))

# set usage
r.sadd("post:42:likes", "user_1")
r.sadd("post:42:likes", "user_2")
r.sadd("post:42:likes", "user_3")
r.sadd("post:42:likes", "user_1")

print(r.smembers("post:42:likes"))

r.sadd("friends:user:1", "Ali", "Hina", "sara")
r.sadd("friends:user:2", "Ahmed", "Hina", "sara")

print(r.sinter("friends:user:1", "friends:user:2"))

# sorted sets with scores usage
r.zadd("leaderboard", {"waqas":1000, "ali": 500, "sara":1500})
print(r.zrevrange("leaderboard", 0, 2, withscores=True))
print(r.zrevrank("leaderboard", "waqas"))
r.zincrby("leaderboard", 1000, "waqas")
print(r.zrevrange("leaderboard", 0, 2, withscores=True))

# json storage
data = {"name":"Muhtasham", "age":21}
r.set("user", json.dumps(data), ex=3600)
cached = r.get("user")
print(json.loads(cached))

# clearing everything from memory
r.flushdb()