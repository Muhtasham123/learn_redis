import redis
import json
from time import sleep
import secrets

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
# Pretend this is your database
FAKE_DB = {
    1: {"id": 1, "name": "Laptop", "price": 50000, "category": "Electronics"},
    2: {"id": 2, "name": "Hammer", "price": 500, "category": "Tools"},
    3: {"id": 3, "name": "Book", "price": 1200, "category": "Education"},
}

FAKE_USERS = {
    "admin@test.com": {"id": 1, "name": "Muhtasham", "password": "123456"},
    "ali@test.com": {"id": 2, "name": "Ali", "password": "abcdef"},
}

#GET PRODUCT FUNCTION --- key_format = product:id --- value will be a json
def get_product(product_id, user_id):
    try:
        # Check if product is in cache
        cached = r.get(f'product:{product_id}')

        if cached:
            print("CACHE HIT")
            return json.loads(cached)

        # If product is not found in cache, fetch, add to cache and then return
        print("CACHE MISS")

        # Using mutex lock to prevent cache stampede
        lock = r.set(f'lock:product:{product_id}', f'{user_id}', nx=True, ex=1)

        if lock:
            db_product = FAKE_DB.get(product_id)

            # preventing cache penetration
            if db_product:
                r.set(f'product:{product_id}', json.dumps(db_product), ex=3600)
            else:
                r.set(f'product:{product_id}', "null", ex=300)

            r.delete(f'lock:product:{product_id}')

            return db_product

        else:
            # Wait while the first user loads product in cache
            sleep(1)

            cached = r.get(f'product:{product_id}')

            if cached and cached != "null":
                print("CACHE HIT AFTER WAITING!")
                return json.loads(cached)

            elif cached == "null":
                return None

            # fallback
            else:
                return FAKE_DB.get(product_id)
    
    except Exception as e:
        print("ERROR", e)

#UPDATE PRICE FUNCTION
def update_price(product_id, new_price):
    try:
        # update price in db
        product = FAKE_DB.get(product_id)
        if product:
            product["price"] = new_price

        # delete key from redis
        r.delete(f'product:{product_id}')

    except Exception as e:
        print("ERROR", e)

#INCREMENT PRODUCT VIEWS FUNCTION
def increment_views(product_id):
    try:
        r.incr(f'product:{product_id}:views')
        # background worker will sync with DB

    except Exception as e:
        print("ERROR", e)


#RATE LIMITER
MAX_REQUESTS = 10
def rate_limiter(ip):
    try:
        count = r.incr(f'requests:{ip}')

        if count == 1:
            r.expire(f'requests:{ip}', 60)

        if count > MAX_REQUESTS:
            return False

        return True
    
    except Exception as e:
        print("ERROR", e)


#SESSION STORAGE
def login(email, password):
    try:
        # verify credentials from DB
        user = FAKE_USERS.get(email)
        if user is None or password != user.get("password"):
            return "Invalid credentials"

        # Else create  token and store a session in redis
        token = secrets.token_hex(16)
        r.set(f'session:{token}', json.dumps({"id":user["id"], "name":user["name"]}), 3600)
        return token

    except Exception as e:
        print("ERROR", e)

#AUTHORIZE TOKEN
def get_me(token):
    try:
        session = r.get(f'session:{token}')

        if session:
            return json.loads(session)
        
        return "Not autorized"

    except Exception as e:
        print("ERROR", e)


#LIKES INCREMENT
def incement_likes(product_id, user_id):
    try:
        r.sadd(f'likes:{product_id}', user_id)
        # background worker will sync with db
    except Exception as e:
        print("ERROR", e)

#GET LIKES OF A PRODUCT
def get_likes(product_id):
    try:
        return r.scard(f'likes:{product_id}')
    except Exception as e:
        print("ERROR", e)