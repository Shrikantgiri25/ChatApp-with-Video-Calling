# chitchat/utils/redis_user_status.py
import redis
from django.conf import settings

r = redis.Redis(host="localhost", port=6379, db=4)


def mark_user_online(user_id):
    r.set(f"user:{user_id}:online", 1, ex=60)


def is_user_online(user_id):
    return r.exists(f"user:{user_id}:online")


def mark_user_offline(user_id):
    r.delete(f"user:{user_id}:online")
