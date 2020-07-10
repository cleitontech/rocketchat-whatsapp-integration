# Rocket.chat integrated with WhatsApp

![](media/demo.gif)

This service sits between [Rocket.chat](rocket.chat) and [chat-api](chat-api.com).
The goal of this project is to be able to integrate rocket chat and whatsapp seamlessly;
allowing both whatsapp users and rocket.chat users to share images, audio, video and text.
This solution is helpful for companies looking for centralizing their customer support, as
it is very commom to have both a chat widget on the company's website, and users who prefer
to use whatsapp as a customer support channel.

## What this project is not.
This project is not related to an official WhatsApp message broker, nor do I or anyone involved
in this project offer any official message broker service.

## Running this project
To run this project you will need:
- a [chat-api](https://chat-api.com/) account
- a server where you can host the project. A free server such as heroku will do the job.
- a server running [rocket.chat](https://rocket.chat)

Once you have all of the items above, you can rename the constants.example.py file to constants.py and add your chat-api
instance number, rocket chat url etc.

Go to your [chat api dashboard](https://app.chat-api.com/dashboard), and under Instance settings,
configure the webhook to ```https://your-domain-name.com/webhook/chatapi?token=your-secret-webhook-token```. This is the endpoint that 
awaits for a post message from chat-api, and forwards it to rocket.chat.

Now every message sent to your chat-api whatsapp number should be
forwarded to your rocket.chat live-messages. But the messages sent from rocket-chat will not 
reach your whatsapp number. To solve this, you need to configure rocket.chat's live message
webhooks found under omnichannel > webhooks > send request for agent's messages. 
Your webhook url should look like ```https://your-domain-name.com/webhook/rocket_chat```.
Make sure to enable rocketchat's webhook secret token. Rocket chat sends this token as a header called ```X-Rocketchat-Livechat-Token```. 

## About messages being lost...
This service relies on both RocketChat's and Chat-Api's webhooks. If your server goes down during the exchange of messages between a WhatsApp client and a RocketChat agent, the message would be lost. If RocketChat's webhook fails to deliver, it retries for ten times every ten minutes. **ChatApi's webhook only tries once,** and if it fails, it completely gives up on delivering that message via webhook. For this reason, a routine was added to store every message's id from ChatApi, until we're sure it was delivered. The routine also periodically requests ChatApi for a list of messages exchanged since the timestamp stored in the ```timestamp.lock``` file (this timestamp is updated every time this routine runs). Finally, if losing messages worries you, I would suggest scheduling a crontab job, that runs the ```queue.sh``` script periodically.

## About media messages expiry 
Media messages sent from WhatsApp are stored in a FireStorage server by ChatApi. These files are kept for 30 days, and then deleted. To circumvent this, media messages are being stored locally by this service and kept for as long as needed.

## TODO:
- [x] Send text messages from WhatApp to Rocket.Chat
- [x] Send text messages from Rocket.chat to WhatsApp
- [x] Send media messages from Rocket.chat to WhatApp
  - [x] images
  - [x] audio
  - [x] documents
- [ ] Send media messages from WhatsApp to Rocket.Chat
  - [x] send media as links
  - [ ] send images as attachments
- [ ] Integrate with other APIs. (e.g., [Wassenger](https://www.wassenger.com/))

## Want to contribute?
Feel free to open a pull request with a bug fix or a feature you think is interesting. 
