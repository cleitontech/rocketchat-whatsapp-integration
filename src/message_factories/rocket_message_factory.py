import json
import os
import requests
import uuid
from src.constants import *
from datetime import date
class RocketMessageFactory:
    def __build_text_message(self):
        return {
            "token": self.visitor["visitor"]["token"],
            "rid": self.room["_id"],
            "msg": self.message["body"],
        }

    def __build_media_message(self):
        print("building media message")
        attachment_type = "image_url"
        #/static/media_upload/2020/07/09/uuid.extension
        url = self.message["body"]
        r = requests.get(url, allow_redirects = True)
        file_extension = url.split("?")[0].split(".")[-1]

        print("the original media url is", self.message["body"])
        print("The file extension is:", file_extension)
        if file_extension.isalnum() and len(file_extension) < 6 and file_extension != "bin":
            file_uuid = str(uuid.uuid4())
            file_relative_path = "{}/{}/{}/".format(
                date.today().year,
                date.today().month,
                date.today().day,
            )
            filepath = MEDIA_UPLOAD_PATH + file_relative_path
            if not os.path.isdir(filepath):
                os.makedirs(filepath)
            open(filepath + file_uuid + "." + file_extension, "wb").write(r.content)
            
            payload = {
                "token": self.visitor["visitor"]["token"],
                "rid": self.room["_id"],
                "msg": "{}{}{}.{}".format(MEDIA_UPLOAD_URL, file_relative_path, file_uuid, file_extension),
            }
            return payload
        else:
            return {
                "token": self.visitor["visitor"]["token"],
                "rid": self.room["_id"],
                "msg": self.message["body"],
            }



    def __init__(self, message, room, visitor):
        self.message = message
        self.room = room
        self.visitor = visitor

    def build(self):
        #if "file" in self.message and self.message["file"] is True:
        if self.message["type"] != "chat":
            final_message = self.__build_media_message()
        else:
            final_message = self.__build_text_message()
        return final_message

