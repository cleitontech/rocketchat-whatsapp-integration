#!/bin/bash

# Agende esse script para rodar a cada minuto no cron. O objetivo é 
# recuperar mensagens que falharam para ser entregues através dos 
# webhooks.
# Por favor, observe que o RocketChat possui um limitador de requisições
# por minuto, podendo gerar fila de entrega. Você pode ajustart o limitador
# de requisições para um valor mais adequado se necessário.
# Recomendável configurar a variável mail address para receber notificações
# em casos de falha.
# Depende:
# - Serviço de email local (ex: postfix)
# - apt install bsd-mailx (app de email)

server_address="http://localhost:5000"
mail_address=
mail_body=/tmp/message-queue-report
>$mail_body

curl -s "${server_address}/chatapi/from-timestamp" >/dev/null 2>&1

message_path=messages_queue/rocket_chat/
for i in $(/usr/bin/find  ${message_path} -type f -mmin +1)
do 
	echo === rocket-chat-queue >> $mail_body
    echo ${i/${message_path}/} >> $mail_body
    cat $i >> $mail_body
    echo >> $mail_body
    curl -X POST -H "Content-Type: application/json" "${server_address}/msg_snd?message_uuid=${i/${message_path}/}"
done

message_path=messages_queue/chat_api/
for i in $(/usr/bin/find  ${message_path} -type f -mmin +1)
do 
    #echo ${i/${message_path}/}
	echo === chat-api-queue >> $mail_body
    echo ${i/${message_path}/} >> $mail_body
    cat $i >> $mail_body
    echo >> $mail_body
    curl -X POST -H "Content-Type: application/json" "${server_address}/msg_recv?message_uuid=${i/${message_path}/}"
done

if [ -s $mail_body ]
then 
    [ -n "$mail_address" ] && mail -s "Queue retry notification: $(date)" $mail_address < $mail_body
fi

