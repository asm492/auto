def insert_db(res):
    myclient = pymongo.MongoClient(DBLINK)
    mydb = myclient["mydb"]
    mycol = mydb["scans"]
    mycol.insert_one(res)