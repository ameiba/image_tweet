# -*- coding: utf-8 -*-
from requests_oauthlib import OAuth1Session
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import sys
import json


#####変更箇所#################
CONSUMER_KEY=""
CONSUMER_SECRET=""
ACCESS_TOKEN_KEY=""
ACCESS_TOKEN_SECRET=""
#ツイートに添付したいファイル名
file_name="000.jpg"       
############################

#pydriveインスタンス作成
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth) 

#GoogleDriveのファイルリストを取得
file_list = drive.ListFile().GetList()
for f in file_list:
    print(f["title"])

image_id = ""
for f in file_list:
    #指定ファイル名があったらID取得
    if f['title'] == file_name:
        image_id = f['id']
        break

#OAuth1Sessionインスタンス作成
twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)

#GoogleDriveの画像をTwitterサーバーにアップロード
image_url = "https://drive.google.com/uc?id=" + image_id
#"http://drive.google.com/uc?export=view&id="
response = requests.get(image_url)
image = response.content
files = {"media" : image}
req_media = twitter.post("https://upload.twitter.com/1.1/media/upload.json", files = files)
if req_media.status_code != 200:
    print ("画像アップロード失敗: %s", req_media.text)
    sys.exit()
    
#アップロードした画像のID取得
media_id = json.loads(req_media.text)['media_id']

#ツイート(複数画像をアップロードする場合は["test1.jpg,test2.jpg"])みたいな感じ
params = {'status': "テスト","media_ids": [media_id]}
req=twitter.post("https://api.twitter.com/1.1/statuses/update.json", params = params)
if req.status_code != 200:
    print ("ツイート失敗: %s", req.text)
    sys.exit()
print("完了")

    