#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
from flask import Flask, request
app = Flask(__name__)

# 截取字符串
def subString(str, start, end, startInd = 0):
  startIndex = str.find(start, startInd)
  if (startIndex == -1): return ''
  # print(startIndex)
  endIndex = str.find(end, startIndex + 1)
  if (endIndex == -1): return ''
  # print(endIndex)
  # print(str[startIndex + len(start):endIndex])
  return str[startIndex + len(start):endIndex]

# 截取字符串组
def subStringArr(str, start, end):
  arr = []
  nextIndex = 0
  while True:
    nextIndex = str.find(start.decode('utf-8'), nextIndex + 1)
    if nextIndex == -1:
      return arr
    temp = subString(str, start, end, nextIndex)
    if str == '':
      return arr
    arr.append(temp)


@app.route('/gps/<ip>')
def index(ip):
  if (ip):
    # 没有headers会返回页面不存在
    headers = {
      "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }
    res = requests.get('http://www.gpsspg.com/ip/?q=' + ip , headers = headers)
    res.encoding = 'utf-8'
    # print(res.text)
    gps = subString(res.text, 'target="_blank">', "</a>").split(",")
    returnData = {
      "ip": subString(res.text, '<span class="fcr">', "</span>"),
      "position": subString(res.text, '<span class="fcg">', "</span><br />"),
      "longitude": gps[0],
      "latitude": gps[1]
    }
    return json.dumps(returnData)
  return ''
  

if __name__ == '__main__':
  app.run(host="0.0.0.0" , port=5000)