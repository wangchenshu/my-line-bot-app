import json
import tornado.web
import urllib
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import define, options
import message

define("channel_url", default="http://127.0.0.1", help="chennel url", type=str)
define("event_path", default="/v1/event", help="event path", type=str)
define("channel_id", default="", help="", type=str)
define("channel_secret", default="", help="", type=str)
define("channel_mid", default="", help="", type=str)
define("event_to_channel_id", default="", help="", type=int)
define("event_type", default="", help="", type=str)

class CallbackHandler(tornado.web.RequestHandler):
    def handle_request(self, response):
        if response.error:
            print "Error:", response.error
        else:            
            print response.body

    def get(self):
        self.write("callback")

    def post(self):
        json_data = json.loads(self.request.body)

        content = json_data['result'][0]["content"]        
        print(content)
        print("from: " + content["from"])

        http_client = AsyncHTTPClient()
        
        if content["text"] in message.send_text:
            send_text = message.send_text[content["text"]]
            markup_json = {
                "canvas": {
                    "width": 1040,
                    "height": 1040,
                    "initialScene": "scene1"
                },
                "images": {
                    "image1": {
                        "x": 0,
                        "y": 0,
                        "w": 1040,
                        "h": 1040
                    }
                },
                "actions": {
                    "openHomepage": {
                        "type": "web",
                        "text": "Open our homepage.",
                        "params": {
                            "linkUri": message.image_link[content["text"] + "_logo"] + "/1020"
                        }
                                     },
                      "showItem": {
                          "type": "web",
                          "text": "Show item.",
                          "params": {
                              "linkUri": message.image_link[content["text"] + "_logo"] + "/1020"
                          }
                      }
                },
                "scenes": {
                    "draws": [
                        {
                            "image": "image1",
                            "x": 0,
                            "y": 0,
                            "w": 1040,
                            "h": 1040
                        }
                    ],
                    "listeners": [
                        {
                            "type": "touch",
                            "params": [0, 0, 1040, 350],
                            "action": "openHomepage"
                        },
                        {
                            "type": "touch",
                            "params": [0, 350, 1040, 350],
                            "action": "showItem"
                        }
                    ]            
                }
            }

            print(message.content_type["rich_messages"])
            send_data = {
                "to": [content["from"]],
                "toChannel": options.event_to_channel_id,
                "eventType": options.event_type,
                "content": {
                    "contentType": message.content_type["rich_messages"],
                    "toType": 1,
                    "contentMetadata": {
                        "DOWNLOAD_URL": message.image_link[content["text"] + "_logo"],
                        "SPEC_REV": "1",
                        "ALT_TEXT": "Please visit our homepage and the item page you wish.",
                        "MARKUP_JSON": json.dumps(markup_json)
                    }
                }
            }
        else:
            send_text = message.send_text["default"]
            send_data = {
                "to": [content["from"]],
                "toChannel": options.event_to_channel_id,
                "eventType": options.event_type,
                "content": {
                    "contentType": message.content_type["text_messages"],
                    "toType": 1,
                    "text": send_text
                }          
            }
            
        print(send_data)

        data = urllib.urlencode(send_data)
        url = options.channel_url + options.event_path
        headers = { 
            'Content-Type': 'application/json',  
            'X-Line-ChannelID': options.channel_id,
            'X-Line-ChannelSecret': options.channel_secret,
            'X-Line-Trusted-User-With-ACL': options.channel_mid
        }
        print(headers)

        http_client.fetch(
            HTTPRequest(url, 'POST', headers, body=json.dumps(send_data)),
            self.handle_request
        )

        self.write("callback")
