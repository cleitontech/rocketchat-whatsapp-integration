from src.constants import *

def create_visitor(message):
    return {
        "visitor":{
            "name": message["chatName"],
            "email": "",
            "token": message["chatId"].replace('@', '-'),
            "department": "",
            "customFields": [
                {
                    "key": "whatsapp_name",
                    "value": message["senderName"],
                    "overwrite": False,
                },
                {
                    "key": "whatsapp_number",
                    "value": message["chatName"],
                    "overwrite": False,
                }
            ]
        }
    }

def get_visitor_url():
    return "{}{}".format(ROCKET_URL_PREFIX, ROCKET_VISITOR_POSTFIX)

def get_room_url(visitor_token, chat_id):
    # check if there is a file with the visitor id
    # if there is a file, get its content and use as the rid
    # check if the room opened rid is the same as the intended rid
    # if not, overrwrite/write the file.
    url="{}{}?token={}&rid={}".format(ROCKET_URL_PREFIX, ROCKET_GET_ROOM_POSTFIX, visitor_token, chat_id)
    return url

def get_rocket_message_url():
    return "{}{}".format(ROCKET_URL_PREFIX, ROCKET_MESSAGE_URL_POSTFIX)


