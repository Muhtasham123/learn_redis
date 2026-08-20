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
# set usage
# set with scores usage
# json storage
# some utility commands