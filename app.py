from flask import Flask, request
import requests
from datetime import datetime
import os
import uuid
import re
from src.message_factories.chat_api_message_factory import ChatApiMessageFactory
from src.message_factories.rocket_message_factory import RocketMessageFactory
from src.urls.chat_api_urls import chat_api_url_factory
from src.urls.rocket_chat_urls import *
from src.visitor_management.visitor_map import *
from src.constants import *
from src.constants import domain_name
from pydub import AudioSegment
from src.messages_queue.messages_queue import *
import json
import time

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static',
            )


@app.route("/chatapi/from-timestamp", methods=["GET"])
def get_all_messages_since():
    min_time = str(open("timestamp.lock", "r").read())
    timestamp_test = datetime.fromtimestamp(int(min_time))

    endpoint = "https://api.chat-api.com/instance{}/messages?token={}&min_time={}".format(
        INSTANCE_ID, CHAT_API_TOKEN, min_time)

    response = requests.get(url=endpoint)
    response = json.loads(response.text)
    messages = response["messages"]
    from_chat_api = [message for message in messages if message["ack"] == 0]

    for message in from_chat_api:
        try:
            id_file = open(CHAT_API_IDS + message["id"], "r")
            id_file.close()
        except:
            file_uuid = str(uuid.uuid4())
            id_file = open(CHAT_API_IDS + message["id"], "w")
            id_file.write(json.dumps(message['id']))
            id_file.close()
            queue_file = open(CHAT_API_QUEUE_FOLDER + file_uuid, "w")
            queue_file.write(json.dumps({"messages": [message]}))
            queue_file.close()
        finally:
            new_timestamp = str(int(time.time()))
            timestamp_file = open(get_messages_timestamp, "w")
            timestamp_file.write(new_timestamp)
            timestamp_file.close()

    return json.dumps("ok")


@app.route('/webhook/rocket_chat/', methods=["GET", "POST"])
def webhook_rocketchat():
    if request.method == 'POST':
        if request.headers["X-Rocketchat-Livechat-Token"] != ROCKETC_WEBHOOK_TOKEN:
            return "Invalid secret token"

        # Create a new message factory to handle different types of
        # possible messages incoming form RocketChat
        messageFactory = ChatApiMessageFactory()

        # extract the payload received via post
        if request.args.get("message_uuid"):
            message_uuid = request.args.get("message_uuid")
            file_path = ROCKET_QUEUE_FOLDER + message_uuid
            file_temp = open(file_path, "r").read()
            received_message = json.loads(file_temp)
        else:
            received_message = request.json
            message_uuid = str(uuid.uuid4())
            RocketChatMessageQueue.store(received_message, message_uuid)
        if not received_message:
            return "NO MESSAGE"

        phone_pattern = re.compile("[0-9]{8,20}-c.us")
        token = received_message["visitor"]["token"]
        match_result = phone_pattern.match(token)
        if not match_result:
            return "Visitor token was not a chat-api id."

        # get hold of the messages array inside the payload sent by
        messages = received_message["messages"]
        # Extract the message destination from the object. It is in the
        # format 5551998121654-c.us
        message_destination = received_message["visitor"]["token"].split(
            "-")[0]

        # iterate through the messages array. Again, tipically this array
        # only contains one message... so a single iteration...
        for message in messages:
            message_blacklisted = False
            for blacklisted in ROCKETCHAT_MESSAGE_BLACKLIST:
                if blacklisted in message["msg"]:
                    message_blacklisted = True

            if not message_blacklisted:
                # Use our message factory to create a message payload accordingly.
                message_dict = messageFactory.create_message(
                    message, message_destination)

                # Build the url based on the message object
                url = chat_api_url_factory(message)

                # Create the header to send along with our request
                if "sendPtt" in url:
                    headers = {'accept': 'application/json',
                               "Content-type": "application/x-www-form-urlencoded"}
                else:
                    headers = {"Content-type": "application/json"}

                # send the message to Chat-Api
                message_json = json.dumps(message_dict)
                answer = requests.post(url, data=message_json, headers=headers)
                if answer.status_code == 200:
                    RocketChatMessageQueue.delete(message_uuid)

                f = open("{0}/{1}".format(
                    CHAT_API_IDS,
                    json.loads(answer.text)["id"]
                ), "w")
                f.write(json.loads(answer.text)["id"])

            else:
                answer = {"text": "Message blacklisted"}

    return answer.text


# Endpoint that awaits a POST request from the chat-api
@app.route('/webhook/chatapi/', methods=["GET", "POST"])
def webhook_chatapi():

    if request.args.get("token") != CHATAPI_WEBHOOK_TOKEN:
        return "Invalid token"

    # only proceed if the request type is POST
    if request.method == 'POST':
        # extract the payload received via post
        if request.args.get("message_uuid"):
            message_uuid = request.args.get("message_uuid")
            file_path = CHAT_API_QUEUE_FOLDER + message_uuid
            file_temp = open(file_path, "r").read()
            received_message = json.loads(file_temp)
        else:
            received_message = request.json
            message_uuid = str(uuid.uuid4())
            ChatApiMessageQueue.store(received_message, message_uuid)

        if not received_message:
            return "NO MESSAGE"

        # If there is no message member inside the json,
        # ignore the request. Because it is probably a ACK
        # message.
        if not "messages" in received_message:
            return "ACK MESSAGE"

        # Get hold of the messages array
        messages = received_message["messages"]

        # for every message in the object, forward to Rocket.chat
        # tipically this is a size 1 array.
        for message in messages:
            # Check if the ack in the message is 0.
            # Ack zero means that the message was sent.
            # So we ignore anything that is not zero to avoid
            # sending duplicate messages to rocket chat.
            if "ack" in message and message["ack"] != 0:
                return "ACK MESSAGE"

            if message["id"][:4] == "true":
                return "Echo message"

            message_id = message["id"]
            message_id_file = open(CHAT_API_IDS + message_id, "w")
            message_id_file.write(message_id)
            message_id_file.close()

            # register visitor in rocket chat
            visitor_dict = create_visitor(message)
            register_visitor_request = requests.post(
                url=get_visitor_url(), data=json.dumps(visitor_dict))
            try:
                visitor = json.loads(register_visitor_request.text)
                visitor_token = visitor["visitor"]["token"]
            except:
                return "Unable to register visitor."

            # Check if a file has already ben created for this visitor.
            # The file should contain his last rocket chat livechat room id.
            rid = create_visitor_rid_file(visitor)
            room = requests.get(url=get_room_url(visitor_token, rid))
            room = json.loads(room.text)
            if room["success"]:
                room = room["room"]
            else:
                # error while creating the room
                # should decide if gets back to client or what
                if room["error"] == "no-agent-online":
                    messageFactory = ChatApiMessageFactory()
                    message_destination = visitor_token.split("-")[0]
                    message = {
                        'u': {
                            "name": NO_AGENT_NAME,
                        },
                        "msg": NO_AGENT_MESSAGE
                    }
                    message_dict = messageFactory.create_message(
                        message, message_destination)
                    message_json = json.dumps(message_dict)
                    url = chat_api_url_factory(message)
                    headers = {"Content-type": "application/json"}
                    requests.post(url, data=message_json, headers=headers)
                    return("ok")
                    # register the offline livechat form?
                    # https://docs.rocket.chat/api/rest-api/methods/livechat/message#send-a-new-livechat-offline-message

            # If the last room the visitor interacted with was closed, update
            # the file with the new rid, so that the next message will be
            # forwarded correctly.
            update_visitor_rid_file(visitor_token, room, rid)

            # Use a message factory to create the fitting message object
            message_factory = RocketMessageFactory(message, room, visitor)
            converted_message = message_factory.build()

            headers = {
                "Content-Type": "application/json"
            }

            response = requests.post(url=get_rocket_message_url(
            ), data=json.dumps(converted_message), headers=headers)

            if response.status_code == 200:
                ChatApiMessageQueue.delete(message_uuid)

    return(response.text)


def startup():
    app.logger.info("#####")
    app.logger.info("ROCKETCHAT WHATSAPP INTEGRATION")
    app.logger.info("#####")
    app.logger.info("DEBUG {0}".format(app.config['DEBUG']))
    app.logger.info("DOMAIN {0}".format(domain_name))
    app.logger.info("ROCKET_URL_PREFIX {0}".format(ROCKET_URL_PREFIX))
    file_folders = ["static", "/static/media_upload", "temp",
                    CHAT_API_IDS, CHAT_API_QUEUE_FOLDER, ROCKET_QUEUE_FOLDER]
    for folder_name in file_folders:
        if not os.path.isdir(os.path.join(os.getcwd(), folder_name)):
            try:
                os.makedirs(os.path.join(os.getcwd(), folder_name))
            except PermissionError:
                print("no permission to create ",
                      os.path.join(os.getcwd(), folder_name))

    get_messages_timestamp = "timestamp.lock"

    try:
        last_message_timestamp = int(open(get_messages_timestamp, "r").read())
        timestamp_test = datetime.fromtimestamp(last_message_timestamp)
    except:
        timestamp_file = open(get_messages_timestamp, "w")
        last_message_timestamp = str(int(time.time()))
        timestamp_file.write(last_message_timestamp)
        timestamp_file.close()


app.before_first_request(startup)

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
