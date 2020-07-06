#!/bin/bash

message_path=messages_queue/rocket_chat/
for i in $(/usr/bin/find  ${message_path} -type f -mmin +1)
do 
	#echo ${i/${message_path}/}
    curl -X POST -H "Content-Type: application/json" "http://localhost:5000/msg_snd?message_uuid=${i/${message_path}/}"
done

message_path=messages_queue/chat_api/
for i in $(/usr/bin/find  ${message_path} -type f -mmin +1)
do 
    #echo ${i/${message_path}/}
    curl -X POST -H "Content-Type: application/json" http://localhost:5000/msg_recv
done


