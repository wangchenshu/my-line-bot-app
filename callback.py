import json
import tornado.web
import urllib
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.options import define, options

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
        send_data = {
            "to": [content["from"]],
            "toChannel": options.event_to_channel_id,
            "eventType": options.event_type,
            "content": {
              "contentType": 1,
              "toType": 1,
              "text": "Hello, Walter at Hex Networks!"
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
