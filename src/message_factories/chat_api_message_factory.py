from src.constants import *
import json
import tempfile
from src.file_handlers.file_converter import *

class ChatApiTextMessage:
    def __init__(self, message_content, destination):
        self.message_content = message_content
        self.destination = destination

    def build(self):
        return {"phone": self.destination, "body": self.message_content}

class ChatApiMediaMessage:
    def __init__(self, public_path, description, destination, file_name, file_type):
        self.public_path = public_path
        self.description = description
        self.destination = destination
        self.file_type = file_type
        self.file_name = file_name

    def build(self):
        if(self.file_type == "audio/mp3"):
            encoded_file = convert_mp3_ogg(self.public_path)
            audio = "data:audio/ogg;base64," + encoded_file
            return {"phone": self.destination, "audio": audio}
            
        else:
            return {"phone": self.destination, "body": self.public_path, "caption": self.description, "filename": self.file_name}


# Factory class that build messages ready to be sent to 
# Chat Api. 
class ChatApiMessageFactory:
    def __init__(self):
        self.text_content = ""
        self.media_url = ""

    def create_message(self, incoming_message, destination):
        #message object that must be returned
        message_dict = {}
        if "fileUpload" in incoming_message:
            # Get the public path url from the file sent from rocket chat
            #public_path = incoming_message["fileUpload"]["publicFilePath"].replace("localhost:3000", domain_name)
            public_path = incoming_message["fileUpload"]["publicFilePath"]

            # the body of the message is the public path
            if "description" in incoming_message["attachments"][0]:
                description = incoming_message["attachments"][0]["description"]
            else:
                description = ""

            file_name = incoming_message["file"]["name"]
            file_type = incoming_message["fileUpload"]["type"]

            # Create a MediaMessage object and return it
            message = ChatApiMediaMessage(public_path, description, destination, file_name, file_type)
            message_dict = message.build()
        else:
            message_content = "*[{}]*\n{}".format(incoming_message["username"], incoming_message["msg"])
            message = ChatApiTextMessage(message_content, destination)
            message_dict = message.build()
        return message_dict

