# -*- coding: utf-8 -*-
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import glob

#例:r"C:\Users\user\desktop\*jpg
#########変更箇所#############
path="path名 + \*jpg"
#############################

#drive準備
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

#ファイル取得
file_list=glob.glob(path)
print(file_list)

#フォルダ作成
f_folder = drive.CreateFile({'title': 'image_folder','mimeType': 'application/vnd.google-apps.folder'})
f_folder.Upload()

folder_id = drive.ListFile({'q': 'title = "image_folder"'}).GetList()[0]['id']

#GoogleDriveに画像をアップロード
for file in file_list:
    name = os.path.basename(file)
    f = drive.CreateFile({'title': name , 'mimeType': 'image/jpeg', 'parents': [{'kind': 'drive#fileLink','id': folder_id}]})
    f.SetContentFile(file)
    f.Upload()
