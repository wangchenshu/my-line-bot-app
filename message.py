#!/usr/bin/env python
#-*- coding: utf-8 -*-

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
    "h4": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/h4-logo",
    "emacs": "https://s3-ap-northeast-1.amazonaws.com/walter-s3/line-bot/image/emacs-logo"
}

send_text = {
    "default": "Welcome to h4!",
    "h4": "Welcome to h4!",
    "emacs": "Welcome to Emacs Taiwan!",
    "how_are_you_today": "How are you today?",
    "where_is_h4": u"""
        餐廳：田中園光華店
        地址：台北市中正區臨沂街 1 號
        (捷運忠孝新生站一號出口直走第一個路口右轉)
        時間：7:30pm ~ 10:00pm

        Restaurant : 田中園 (Tian Jung Yuan)
        Venue : No. 1, Linyi St, Zhongzheng District, Taipei City
        (MRT JungXiao Xingshen Station Exit 1)
        Time : 7:30pm ~ 10:00pm
    """,
    "what_are_h4_people_do": u"""
        1. 討論 web, network, programming, system, blablah….
        2. 交流系統工具 & 使用技巧
        3. 八卦
    """,
    "h4_beginning": u"""
        Hacking Thursday 是由幾位居住於台北地區的自由軟體/開放原碼開發者所發起，
        每週四晚上會於特定咖啡店聚會。以非會議形式、交換並實做各自提出的想法，
        輕鬆的會議過程以禮貌、謙遜與尊重的互信態度接納並鼓勵概念發想、發起新計畫、
        並從開發者的協同開發與經驗分享中互相學習。
    """,
    "contact_us": u"""
        除了實體聚會外，我們使用 Google group / Facebook group 做為大家的溝通聯絡管道。
        聊天，討論，及聚會通告都會在這裡發佈。如果您對我們的聚會有興趣，隨時都歡迎您加入/訂閱我們的討論區，和我們交流！！

        http://groups.google.com/group/hackingthursday ( Google group )
        http://www.facebook.com/groups/hackingday/ ( Facebook group )
        https://www.meetup.com/hackingthursday/ ( Meetup )
    """
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
