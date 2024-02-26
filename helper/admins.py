import pymongo
from config import Config



dbclient = pymongo.MongoClient(Config.DB_URL)
database = dbclient[Config.DB_NAME]

admins_collection = database['admins']


async def add_admin(user_id: int):
    try:
        admins_collection.insert_one({'_id': user_id})
        return True
    except Exception as e:
        print(f"Failed to add admin: {e}")
        return False

# Function to remove aa user from admin
async def remove_admin(user_id: int):
    try:
        admins_collection.delete_one({'_id': user_id})
        return True
    except Exception as e:
        print(f"Failed to remove admin: {e}")
        return False

# Function to check if a user is an admin
async def is_admin(user_id: int):
    return bool(admins_collection.find_one({'_id': user_id}))

async def get_admin_list():
    admin_docs = admins_collection.find()
    admin_ids = [doc['_id'] for doc in admin_docs]
    return admin_ids
