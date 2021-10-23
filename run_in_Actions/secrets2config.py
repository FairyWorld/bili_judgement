# -*- coding: utf-8 -*-
# 用Secrets生成配置文件config.json

import json5, os, re, traceback
from collections import OrderedDict

ADVCONFIG: str = os.environ.get('ADVCONFIG', None)

if ADVCONFIG:
    print("已配置ADVCONFIG，用于覆盖config.json文件")
    with open('./config/config.json','w',encoding='utf-8') as fp:
        fp.write(ADVCONFIG)

BILICONFIG: str = os.environ.get('BILICONFIG', None)
PUSH_MESSAGE: str = os.environ.get('PUSH_MESSAGE', None)

if not (BILICONFIG or ADVCONFIG):
    print("完成最后检查，现在开始任务")
    exit(-1)

try:
    with open('./config/config.json','r',encoding='utf-8') as fp:
        configData: str(dict = json5.load(fp, object_pairs_hook=OrderedDict))
except:
    print(f'配置文件加载失败，原因为({traceback.format_exc()})')
    print(f'此错误是由于配置文件不符合json5(json)格式导致的，如果您不了解json规范，建议您恢复config/config.json文件，删除advconfig(如果配置过)，仅使用biliconfig和push_message(可选)两个secrets')
    exit(-1)

if BILICONFIG:
    print("发现biliconfig，开始映射cookie")
    SESSDATA, bili_jct, DedeUserID = False, False, False
    users = []
    cookieDatas = {}
    for ii, x in enumerate(BILICONFIG.split("\n")):
        cookie = x.strip().replace(",", "%2C").replace("%2A", "*")
        if re.match("[a-z0-9]{8}%2C[0-9a-z]{10}%2C[a-z0-9]{5}.[a-z0-9]{2}", cookie):
            cookieDatas["SESSDATA"] = cookie
            SESSDATA = True
            print(f'biliconfig第{ii+1}行解析为SESSDATA')
        elif re.match("[a-z0-9]{31}", cookie):
            cookieDatas["bili_jct"] = cookie
            bili_jct = True
            print(f'biliconfig第{ii+1}行解析为bili_jct')
        elif re.match("^[0-9]{5,}$", cookie):
            cookieDatas["DedeUserID"] = cookie
            DedeUserID = True
            print(f'biliconfig第{ii+1}行解析为DedeUserID')
        else:
            print(f'biliconfig第{ii+1}行不能解析为cookie，跳过本行')
        if SESSDATA and bili_jct and DedeUserID:
            users.append({"cookieDatas": cookieDatas.copy(), "tasks": {}})
            SESSDATA, bili_jct, DedeUserID = False, False, False
            print(f'biliconfig成功添加1个账号')
    if len(users) == 0:
        print("虽然配置了BILICONFIG，但并没有发现有效账户cookie")
        exit(-1)
    else:
        configData["users"] = users

if PUSH_MESSAGE:
    print("发现push_message，开始映射到webhook消息推送")
    ADVCONFIG: str = os.environ.get('ADVCONFIG', None)

with open('./config/config.json','w',encoding='utf-8') as fp:
    json5.dump(configData, fp, ensure_ascii=False)
