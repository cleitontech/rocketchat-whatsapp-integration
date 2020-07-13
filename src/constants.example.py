import os

domain_name = os.environ.get(
    "domain_name", "your.domain.com"
)
MEDIA_UPLOAD_URL = os.environ.get(
    "MEDIA_UPLOAD_URL", "https://{0}/static/media_upload/".format(domain_name)
)

MEDIA_UPLOAD_PATH = os.environ.get(
    "MEDIA_UPLOAD_PATH", os.path.join(os.getcwd(), "static/media_upload/")
)

# CHAT API ENDPOINTS
CHAT_API_URL = os.environ.get(
    "CHAT_API_URL", 'https://euXXX.chat-api.com/instanceXXXXXX/'
)

INSTANCE_ID = os.environ.get("INSTANCE_ID", 'XXXXXX')
CHAT_API_TOKEN = os.environ.get("CHAT_API_TOKEN", 'kj1h23kj1h232')

# check https://chat-api.com/en/docs_beta.html#/messages/getFile for more.
CHAT_GET_FILE = os.environ.get("CHAT_GET_FILE", "/getFile?msgId={}&token={}")


# ROCKET CHAT ENDPOINTS
ROCKET_URL_PREFIX = os.environ.get(
    "ROCKET_URL_PREFIX", 'http://your-rocket-chat-domain'
)
ROCKET_MESSAGE_URL_POSTFIX = os.environ.get(
    "ROCKET_MESSAGE_URL_POSTFIX", '/api/v1/livechat/message'
)
ROCKET_GET_ROOM_POSTFIX = os.environ.get(
    "ROCKET_GET_ROOM_POSTFIX", '/api/v1/livechat/room')

ROCKET_VISITOR_POSTFIX = os.environ.get(
    "ROCKET_VISITOR_POSTFIX", "/api/v1/livechat/visitor")


CHAT_API_QUEUE_FOLDER = os.environ.get(
    "CHAT_API_QUEUE_FOLDER", "messages_queue/chat_api/"
)

ROCKET_QUEUE_FOLDER =  os.environ.get(
    "ROCKET_QUEUE_FOLDER", "messages_queue/rocket_chat/"
)

CHAT_API_IDS = os.environ.get(
    "CHAT_API_IDS", "messages_received_chat_api/"
)

ROCKETCHAT_MESSAGE_BLACKLIST = ["Chat encerrado pelo agente"]

# SECRET TOKENS
CHATAPI_WEBHOOK_TOKEN = os.environ.get(
    "CHATAPI_WEBHOOK_TOKEN", "secret1"
)
ROCKETC_WEBHOOK_TOKEN = os.environ.get(
    "ROCKETC_WEBHOOK_TOKEN", "secret2"
)

# NO AGENT CONFIGS
NO_AGENT_NAME = os.environ.get(
    "NO_AGENT_NAME", "NO AGENTS"
)
NO_AGENT_MESSAGE = os.environ.get(
    "NO_AGENT_MESSAGE",
    '''Sorry! No Agents right now. We have registered your message and will
get back as soon as possible'''
)