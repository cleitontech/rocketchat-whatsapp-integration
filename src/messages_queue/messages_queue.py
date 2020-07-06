import os
import json
from src.constants import CHAT_API_QUEUE_FOLDER, ROCKET_QUEUE_FOLDER
class ChatApiMessageQueue:
    @staticmethod
    def store(received_message, message_uuid):
        message_content = json.dumps(received_message)
        file_path = CHAT_API_QUEUE_FOLDER + str(message_uuid)
        message_file = open(file_path, "w")
        message_file.write(message_content)
        message_file.close()

    @staticmethod
    def delete(message_uuid):
        file_path = CHAT_API_QUEUE_FOLDER + message_uuid
        if(os.path.isfile(file_path)):
            try:
                os.remove(file_path)
            except:
                print("Couldn't delete file:", file_path)
            

class RocketChatMessageQueue:
    @staticmethod
    def store(received_message, message_uuid):
        message_content = json.dumps(received_message)
        file_path = ROCKET_QUEUE_FOLDER + message_uuid
        message_file = open(file_path, "w")
        message_file.write(message_content)
        message_file.close()

    @staticmethod
    def delete(message_uuid):
        file_path = ROCKET_QUEUE_FOLDER + str(message_uuid)
        if(os.path.isfile(file_path)):
            try:
                os.remove(file_path)
            except:
                print("Couldn't delete file:", file_path)

