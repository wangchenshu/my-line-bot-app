#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import tornado.web
import urllib
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import define, options
from tornado import gen
import message

define("channel_url", default="", help="chennel url", type=str)
define("event_path", default="", help="event path", type=str)
define("channel_id", default="", help="", type=str)
define("channel_secret", default="", help="", type=str)
define("channel_mid", default="", help="", type=str)
define("event_to_channel_id", default="", help="", type=int)
define("event_type", default="", help="", type=str)
define("get_user_profile_path", default="", help="", type=str)

class CallbackHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        json_data = json.loads(self.request.body)
        content = json_data['result'][0]["content"]

        print(content)
        print("from: " + content["from"])

        http_client = AsyncHTTPClient()
        content_text = content["text"].lower()
        send_text = message.send_text["default"]

        if content_text in message.image_link:
            send_text = message.send_text[content_text]
            send_data = message.create_rich_messages(
                [content["from"]],
                options.event_to_channel_id,
                options.event_type,
                "rich_messages",
                message.image_link[content_text],
                message.image_link[content_text],
                json
            )
        else:
            if "h4" in content_text and                                                       \
               ("where" in content_text or "go" in content_text or "going" in content_text or \
                u"如何去" in content_text or u"怎麼去" in content_text or                     \
                u"如何走" in content_text or u"怎麼走" in content_text):
                send_text = message.send_text["where_is_h4"]

            elif "h4" in content_text and ("doing" in content_text or u"做什麼" in content_text):
                send_text = message.send_text["what_are_h4_people_do"]

            elif "h4" in content_text and u"由來" in content_text:
                send_text = message.send_text["h4_beginning"]

            elif "contact" in content_text or u"聯絡" in content_text:
                send_text = message.send_text["contact_us"]

            send_data = message.create_text_message(
                [content["from"]],
                options.event_to_channel_id,
                options.event_type,
                "text_messages",
                send_text
            )

        data = urllib.urlencode(send_data)
        url = options.channel_url + options.event_path
        headers = { 
            'Content-Type': 'application/json',  
            'X-Line-ChannelID': options.channel_id,
            'X-Line-ChannelSecret': options.channel_secret,
            'X-Line-Trusted-User-With-ACL': options.channel_mid
        }

        print(send_data)

        try:
            user_profile_response = yield http_client.fetch(
                HTTPRequest(
                    options.channel_url           + \
                    options.get_user_profile_path + \
                    "?mids=" + content["from"],
                    'GET',
                    headers
                )
            )
            user_profile = json.loads(user_profile_response.body)
            user_name = user_profile["contacts"][0]["displayName"]

        except tornado.httpclient.HTTPError as e:
            print("ex: " + str(e))

        except Exception as e:
            print("Error: " + str(e))
        
        if "text" in send_data["content"]:
            send_data["content"]["text"] = "@" + user_name + ": " + send_data["content"]["text"]

        try:
            send_message_response = yield http_client.fetch(
                HTTPRequest(url, 'POST', headers, body=json.dumps(send_data))
            )
    
            if user_profile_response.error:
                print "Error:", user_profile_response.error
            else:
                print 'user profiles: ' + user_profile_response.body + '\n' + \
                      'send_message_response: ' + send_message_response.body

        except tornado.httpclient.HTTPError as e:
            print("ex: " + str(e))

        except Exception as e:
            print("Error: " + str(e))
                    
        self.write("callback")
