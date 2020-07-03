import os
from constants import CHAT_API_QUEUE_FOLDER, ROCKET_QUEUE_FOLDER
class ChatApiMessageQueue:
    @static
    def store(message):
        message = [message]
        message_content = json.dumps(message)
        message_id = message["id"].replace("@", "-").replace(".", "-")
        file_path = CHAT_API_QUEUE_FOLDER + message_id
        message_file = open(message_id, "w")
        message_file.write(message_content)
        message_file.close()

    @static
    def delete(message):
        message_id = message["id"]
        file_path = CHAT_API_QUEUE_FOLDER + message_id
        if(os.path.isfile(file_path)):
            try:
                os.remove(file_path)
            except:
                print("Couldn't delete file:", file_path)

            

class RocketChatMessageQueue:
    @static
    def store(message):
        message_content = json.dumps(message)
        message_id = message["_id"].replace("@", "-").replace(".", "-")
        file_path = ROCKET_QUEUE_FOLDER + message_id
        message_file = open(file_path, "w")
        message_file.write(message_content)
        message_file.close()

    @static
    def delete(message):
        message_id = message["_id"]
        file_path = ROCKET_QUEUE_FOLDER + message_id
        if(os.path.isfile(file_path)):
            try:
                os.remove(file_path)
            except:
                print("Couldn't delete file:", file_path)
