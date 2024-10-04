from utilities.config import db


async def get_chat_history():
    try:
        chat_collection = db.get_collection("chat")

        get_chat = await chat_collection.find().sort("_id", 1).to_list(length=None)
        return get_chat
    except Exception as e:
        print(repr(e))
        return None