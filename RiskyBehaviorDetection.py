# !/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import base64
import requests
import json
from urllib.request import Request,urlopen
from urllib.parse import urlencode,quote


def capture_data_as_mp4(filepath, width, height, fps, timeseconds):
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

    vout = cv2.VideoWriter()
    vout.open(filepath, fourcc, fps, sz, True)

    cnt = 0
    while (cnt // fps < timeseconds):
        cnt += 1
        print(cnt)
        ret, frame = cap.read()
        vout.write(frame)
    vout.release()

def file_str_to_base64(filepath):
    video_code = ""
    with open(filepath, "rb") as file:
        video_code = file.read()
        video_code = base64.b64encode(video_code)
    return video_code


# client_id 为官网获取的AK， client_secret 为官网获取的SK
ak = 'ewuQ93j9hHxVLs6Mc8F2UkKR'
sk = '8LzNbOX2NEALA5kxoufiH8uWpMXWtctN'

# client_id 为官网获取的AK， client_secret 为官网获取的SK
access_token_url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(ak,sk)
response = requests.get(access_token_url)
if response:
    print("access_token= "+response.json()["access_token"])
access_token = response.json()["access_token"]

url = 'https://aip.baidubce.com/rest/2.0/video-classify/v1/body_danger?access_token={}'.format(access_token)
filepath = "./data.mp4"
# capture_data_as_mp4(filepath=filepath, width=680, height=460, fps=30, timeseconds=5)
headers = {}
headers[b'Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'

body={}
body[b"data"] = file_str_to_base64(filepath)
data = urlencode(body).encode("utf-8")
# print("data=" + str(file_str_to_base64(filepath)))

request = Request(url,data,headers=headers)
response = urlopen(request)
responseJson = json.loads(response.read())

print(responseJson)
print(responseJson["result"][0]["name"])

