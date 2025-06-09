
import motor.motor_asyncio
from config import DB_URI, DB_NAME

dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
database = dbclient[DB_NAME]

user_data = database['users']
cmd_data = database['users']

channels_collection = database['channelxyz']
req_collection = database['reqxyz']


default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}

def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }

async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.insert_one(user)
    return

async def db_verify_status(user_id):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def db_update_verify_status(user_id, verify):
    await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] async for doc in user_docs]
    return user_ids

async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})
    return
# Retrieve all force subscription channels from the database
async def get_force_sub_channels():
    """Retrieve all force subscription channels from the database."""
    channels = await channels_collection.find({}).to_list(length=None)
    return [channel['channel_id'] for channel in channels]

async def get_all_force_sub_channels():
    """Retrieve all force subscription channels dynamically."""
    channels = await channels_collection.find({}).to_list(length=None)
    return [{"channel_id": channel["channel_id"]} for channel in channels]

# Add a new force subscription channel
async def add_channel(channel_id: int):
    """Add a new force subscription channel."""
    await channels_collection.update_one(
        {'channel_id': channel_id},
        {'$set': {'channel_id': channel_id}},
        upsert=True
    )

# Remove a force subscription channel
async def remove_channel(channel_id: int):
    """Remove a force subscription channel."""
    result = await channels_collection.delete_one({'channel_id': channel_id})
    return result

# List all force subscription channels
async def list_channels():
    """List all force subscription channels."""
    return await get_force_sub_channels()

# Reset all force subscription channels (clear the collection)
async def reset_channels():
    """Reset all force subscription channels (clear the collection)."""
    await channels_collection.delete_many({})
