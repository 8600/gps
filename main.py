#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import json
# import MySQLdb
from flask import Flask, request
app = Flask(__name__)

@app.route('/gps/<ip>')
def index(ip):
  if (ip):
    # 打开数据库连接
    # db = MySQLdb.connect(host="192.168.0.226",user="root",passwd="GwlF97#6",db="gps",charset="utf8")
    # # 使用cursor()方法获取操作游标 
    # cursor = db.cursor()

    # 没有headers会返回页面不存在
    headers = {
      "cookie": "__cfduid=dc0fd8b83edb2d0deba1e38199a73424f1541080023;",
      "content-type": "application/vnd.maxmind.com-city+json; charset=UTF-8; version=2.1",
      "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }
    res = requests.get('https://www.maxmind.com/geoip/v2.1/city/'+ ip +'?use-downloadable-db=1&demo=1' , headers = headers)
    res.encoding = 'utf-8'
    resData = res.json()
    # print(resData)
    if (not ("city" in resData)): resData["city"] = ""
    if (not ("location" in resData)): resData["location"] = ""
    if (not ("postal" in resData)): resData["postal"] = ""
    if (not ("subdivisions" in resData)): resData["subdivisions"] = ""
    # print(resData)
    data = "'{city}', '{continent}', '{country}', '{location}', '{registered_country}', '{subdivisions}', '{traits}'".format(city=resData["city"],continent=resData["continent"], country=resData["country"], location=resData["location"], registered_country=resData["registered_country"], subdivisions=resData["subdivisions"], traits=resData["traits"])
    print(data)
    # SQL 插入语句
    sql = """INSERT INTO location(city,
            continent, country, location, registered_country, subdivisions, traits)
            VALUES (""" + data +""")"""
    try:
      # 执行sql语句
      cursor.execute(sql)
      # 提交到数据库执行
      db.commit()
    except:
      # Rollback in case there is any error
      db.rollback()

    # 关闭数据库连接
    db.close()
    return res.text
  return ''
  

if __name__ == '__main__':
  app.run(host="0.0.0.0" , port=5000)