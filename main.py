#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
import MySQLdb
from flask import Flask, request
app = Flask(__name__)

# 打开数据库连接
db = MySQLdb.connect(host="192.168.0.226",user="root",passwd="GwlF97#6",db="gps",charset="utf8")

# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")

# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()

print "Database version : %s " % data

# 关闭数据库连接
db.close()

@app.route('/gps/<ip>')
def index(ip):
  print(ip)
  if (ip):
    # 没有headers会返回页面不存在
    headers = {
      "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }
    res = requests.get('https://www.maxmind.com/geoip/v2.1/city/'+ ip +'?use-downloadable-db=1&demo=1' , headers = headers)
    res.encoding = 'utf-8'
    print(res.json())
    # gps = subString(res.json, 'target="_blank">', "</a>").split(",")
    # returnData = {
    #   "ip": subString(res.text, '<span class="fcr">', "</span>"),
    #   "position": subString(res.text, '<span class="fcg">', "</span><br />"),
    #   "longitude": gps[0],
    #   "latitude": gps[1]
    # }
    return res.text
  return ''
  

if __name__ == '__main__':
  app.run(host="0.0.0.0" , port=5000)