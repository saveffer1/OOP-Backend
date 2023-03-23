"""
    mongo db
"""
import pymongo
import configparser

config = configparser.ConfigParser()
config.read("./src/db/config.ini")

client = pymongo.MongoClient(
    f"mongodb+srv://{config['mongodb']['user']}:{config['mongodb']['key']}@db0.xusrgij.mongodb.net/?retryWrites=true&w=majority"
    )
