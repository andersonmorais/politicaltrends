import json as simplejson
import pymongo
import threading
#import config
import os,json

from pymongo import MongoClient

initialized=False
db = None
collection = None   

# Remove all documents from the collection every 24hs
def refresh():
    db.collection.drop()
    threading.Timer(86400, refresh).start()

# Retrieve data from the collection based on the input url or text
def get_trend_data(url, text):
    # If data is in cache, return it
    if text is None:
        cursor = db.collection.find({"url": url})
        if not cursor:
            #print("[DEBUG]: get_trend_data1: cursor {1}")
            #for document in cursor:
            #    print(document)
            return db.collection.find({"url": url})["trends"]
        # Data is not on cache
        else:
            #print("[DEBUG]: get_trend_data2: cursor {1}")
            return False
    if url is None:
        cursor = db.collection.find({"text": text})
        if not cursor:
            return db.collection.find({"text": text})["trends"]
        # Data is not on cache
        else:
            return False  

# Store data in the collection based on the input url or text
def store_trends_data(url, text, trendresult):
    # If data is in cache, return it
    ######################## Crashed on IBM Bluemix 
#     if text is None: 
#         db.collection.insert_one({'url': url, 'trends' : trendresult})
#     elif url is None:
#         db.collection.insert_one({'text': text, 'trends' : trendresult})
    return

# Initialize connection variables
def initialize():
    global initialized
    global db
    global collection
    # If connection is not initialized, initialize it.
    if not initialized:
        ###################### Initialize DB in the cloud ##############################
        vcap_config = os.environ.get('VCAP_SERVICES')
        decoded_config = json.loads(vcap_config)
        for key, value in decoded_config.items():
            if key.startswith('mongodb'):
                mongo_creds = decoded_config[key][0]['credentials']
        mongo_url = str(mongo_creds['url'])
        
        client = MongoClient(mongo_url)
        ################################################################################

        ###################### Initialize DB in localhost ##############################
       
        #config.client = pymongo.MongoClient(host="localhost:27017")
        #client = MongoClient()
#        client = MongoClient('localhost', 27017)
        ################################################################################
        
        #config.db = config.client['db']
        db = client['mongodb1']
        
        #config.collection = config.db['mycollection']
        collection = db['trends']
        
        ######################## Crashed on IBM Bluemix
#        db.collection.drop()
        
        initialized=True
        
        ######################## Crashed on IBM Bluemix        
#        refresh()

