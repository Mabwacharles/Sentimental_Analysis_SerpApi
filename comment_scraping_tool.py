# Scrape Comments for SQL Using Python Through The Youtube Data API

api_key = "AIzaSyDm1N7pLzWgmLM5Ncfjeku9GnpGF4sZIzs" # Replace this dummy api key with your own.

from googleapiclient.discovery import build
youtube = build('youtube', 'v3', developerKey=api_key)

import pandas as pd

box = [['Name', 'Comment', 'Time', 'Likes', 'Reply Count']]

#Eudereka, Programming with Mosh, freeCodeCamp
code_lang = [
    {"id":"HXV3zeQKqGY"},
    {"id":"7S_tz1z_5bA"},
    {"id":"zbMHLJ0dY4w"}
]

# sql_vids = pd.DataFrame([])

for id_code in code_lang:
    def scrape_comments_with_replies():
        data = youtube.commentThreads().list(part='snippet', videoId=id_code['id'], maxResults='100', textFormat="plainText").execute()
        
        for i in data["items"]:
            name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
            comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
            published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
            likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
            replies = i["snippet"]['totalReplyCount']
            
            box.append([name, comment, published_at, likes, replies])
            
            totalReplyCount = i["snippet"]['totalReplyCount']
            
            if totalReplyCount > 0:
                
                parent = i["snippet"]['topLevelComment']["id"]
                
                data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                            textFormat="plainText").execute()
                
                for i in data2["items"]:
                    name = i["snippet"]["authorDisplayName"]
                    comment = i["snippet"]["textDisplay"]
                    published_at = i["snippet"]['publishedAt']
                    likes = i["snippet"]['likeCount']
                    replies = ""

                    box.append([name, comment, published_at, likes, replies])

        while ("nextPageToken" in data):
            
            data = youtube.commentThreads().list(part='snippet', videoId=id_code['id'], pageToken=data["nextPageToken"],
                                             maxResults='100', textFormat="plainText").execute()
                                             
            for i in data["items"]:
                name = i["snippet"]['topLevelComment']["snippet"]["authorDisplayName"]
                comment = i["snippet"]['topLevelComment']["snippet"]["textDisplay"]
                published_at = i["snippet"]['topLevelComment']["snippet"]['publishedAt']
                likes = i["snippet"]['topLevelComment']["snippet"]['likeCount']
                replies = i["snippet"]['totalReplyCount']

                box.append([name, comment, published_at, likes, replies])

                totalReplyCount = i["snippet"]['totalReplyCount']

                if totalReplyCount > 0:
                    
                    parent = i["snippet"]['topLevelComment']["id"]

                    data2 = youtube.comments().list(part='snippet', maxResults='100', parentId=parent,
                                                    textFormat="plainText").execute()

                    for i in data2["items"]:
                        name = i["snippet"]["authorDisplayName"]
                        comment = i["snippet"]["textDisplay"]
                        published_at = i["snippet"]['publishedAt']
                        likes = i["snippet"]['likeCount']
                        replies = ''

                        box.append([name, comment, published_at, likes, replies])

        df = pd.DataFrame({'Name': [i[0] for i in box], 'Comment': [i[1] for i in box], 'Time': [i[2] for i in box],
                       'Likes': [i[3] for i in box], 'Reply Count': [i[4] for i in box]})
        
        sql_vids = pd.DataFrame([])

        sql_vids = sql_vids.append(df, ignore_index = True)

        sql_vids.to_csv('youtube-comments.csv', index=False, header=False)
    
    scrape_comments_with_replies()