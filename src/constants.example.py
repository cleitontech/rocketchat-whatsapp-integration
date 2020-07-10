import os

domain_name                         = "your-domain-name.com"
MEDIA_UPLOAD_URL                    = "http://your-domain:port/static/media_upload/" 
MEDIA_UPLOAD_PATH                    = os.path.join(os.getcwd(), "static/media_upload/") 

# CHAT API ENDPOINTS
CHAT_API_URL                        = 'https://eu200.chat-api.com/instanceXXXXXX'
INSTANCE_ID                         = 'XXXXXX'
CHAT_API_TOKEN                      = 'your-api-token'

# check https://chat-api.com/en/docs_beta.html#/messages/getFile for more.
CHAT_GET_FILE                       = "/getFile?msgId={}&token={}"


# ROCKET CHAT ENDPOINTS
ROCKET_URL_PREFIX                   = 'http://your-rocket-chat-domain'
ROCKET_MESSAGE_URL_POSTFIX          = '/api/v1/livechat/message'
ROCKET_GET_ROOM_POSTFIX             = '/api/v1/livechat/room'
ROCKET_VISITOR_POSTFIX              = "/api/v1/livechat/visitor"

STATIC_FILES_PATH                   = "http://localhost:5000/static/"

CHAT_API_QUEUE_FOLDER               = "messages_queue/chat_api/"
ROCKET_QUEUE_FOLDER                 = "messages_queue/rocket_chat/"
CHAT_API_IDS                        = "messages_received_chat_api/"

ROCKETCHAT_MESSAGE_BLACKLIST        = ["Chat encerrado pelo agente"]

# SECRET TOKENS
CHATAPI_WEBHOOK_TOKEN               = "A secret token you define as a get parameter of the chat api webhook" 
ROCKETC_WEBHOOK_TOKEN               = "A secret token configured in the rocket chat live chat webhook." 
