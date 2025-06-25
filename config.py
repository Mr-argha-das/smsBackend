# config.py
from mongoengine import connect

MONGO_URI = "mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/smsTest"
OPENAI_API_KEY = "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"

connect('smsTest',host=MONGO_URI)
