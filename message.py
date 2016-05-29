
content_type = {
    "text_messages": 1,
    "image_message": 2,
    "video_message": 3,
    "audio_message": 4,
    "location_message": 7,
    "sticker_message": 8,
    "contact_message": 10,
    "rich_messages": 12
}

image_link = {
    "h4_logo": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/h4-logo",
    "emacs_logo_black": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/11813376_842684179173214_3987034703356373870_n.jpg",
    "emacs_logo": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/emacs-logo",
    "debian_logo_small": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/openlogo-100.png"
}

send_text = {
    "default": "Welcome to h4!",
    "h4": "Welcome to h4!",
    "emacs": "Welcome to Emacs Taiwan!",
    "how_are_you_today": "How are you today?"
}

def create_text_message(to, event_to_channel_id, event_type, content_type_key, send_text):
    return {
       "to": to,
       "toChannel": event_to_channel_id,
       "eventType": event_type,
       "content": {
           "contentType": content_type[content_type_key],
           "toType": 1,
           "text": send_text
       }
    }

def create_rich_messages(to, event_to_channel_id, event_type, content_type_key, download_url, image_link, json):
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
                    "linkUri": image_link + "/1040"
                }
                             },
              "showItem": {
                  "type": "web",
                  "text": "Show item.",
                  "params": {
                      "linkUri": image_link + "/1040"
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

    return {
        "to": to,
        "toChannel": event_to_channel_id,
        "eventType": event_type,
        "content": {
            "contentType": content_type[content_type_key],
            "toType": 1,
            "contentMetadata": {
                "DOWNLOAD_URL": image_link,
                "SPEC_REV": "1",
                "ALT_TEXT": send_text["default"],
                "MARKUP_JSON": json.dumps(markup_json)
            }
        }
    }
