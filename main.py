import base64
import datetime
import json
import os
import random
import re
import time

import requests


def bark(device_key, title, content, bark_icon):
    if not device_key:
        return 2

    url = "https://api.day.app/push"
    headers = {
        "content-type": "application/json",
        "charset": "utf-8"
    }
    data = {
        "title": title,
        "body": content,
        "device_key": device_key
    }

    if not bark_icon:
        bark_icon = ''
    if len(bark_icon) > 0:
        url += '?icon=' + bark_icon
        print('拼接icon')
    else:
        print('不拼接icon')

    resp = requests.post(url, headers=headers, data=json.dumps(data))
    resp_json = resp.json()
    if resp_json["code"] == 200:
        print(f"[Bark]Send message to Bark successfully.")
    if resp_json["code"] != 200:
        print(f"[Bark][Send Message Response]{resp.text}")
        return -1
    return 0


def decode_base64(data):
    try:
        decoded_bytes = base64.b64decode(data)
    except base64.binascii.Error:
        decoded_bytes = base64.decodebytes(data.encode('utf-8'))
    decoded_string = decoded_bytes.decode('utf-8')
    return decoded_string


def sign(token, bark_deviceKey, bark_icon):
    if not token:
        print('不执行签到1,token为null')
        return -1

    token = token.strip()
    if len(token) <= 0:
        print('不执行签到2,token为空')
        return -2

    if '.' not in token:
        print('不执行签到3,token格式错误，未包含.')
        return -3

    print('有token，需要执行签到')

    many = token.split('.')
    pay = many[1]
    old = decode_base64(pay + '==')
    res = json.loads(old)

    # jwt的过期时间
    timestamp = res['exp']

    # 获取当前时间并转换为timestamp格式
    current_time = datetime.datetime.now()
    current_timestamp = int(current_time.timestamp())

    title = 'Link.AI-签到结果'
    message = ''

    message_all = []

    # 前面拼接jwt的过期时间
    date_time = datetime.datetime.fromtimestamp(timestamp)
    formatted_date = date_time.strftime('%Y-%m-%d %H:%M:%S')
    message_all.append('jwt.exp：' + formatted_date + '。' + '\n')

    # 比较时间戳与当前时间的关系
    if timestamp > current_timestamp:
        url = 'https://link-ai.tech/api/chat/web/app/user/sign/in'
        headers = {
            'Authorization': 'Bearer ' + token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        print(response.text)

        if "今日已签到" in response.text:
            message_all.append('今日已签到，请明日再来！' + '\n')
        elif "success" in response.text:
            message_all.append('签到成功！' + '\n')
        elif "401" in response.text:
            message_all.append('jwt校验失败，请检查！' + '\n')
        else:
            if len(response.text) > 100:
                message_all.append(response.text[:100] + '\n')
            else:
                message_all.append(response.text + '\n')
    elif timestamp <= current_timestamp:
        message_all.append('请重新登录并更新Github中token的值！' + '\n')

    message_all = '\n'.join(message_all)
    message_all = re.sub('\n+', '\n', message_all).rstrip('\n')
    message = message_all

    bark(bark_deviceKey, title, message, bark_icon)


def main():
    bark_device_key = os.environ.get('BARK_DEVICEKEY')
    bark_icon = os.environ.get('BARK_ICON')
    authorization = os.environ.get('Authorization')

    wait = random.randint(3, 8)
    time.sleep(wait)

    sign(authorization, bark_device_key, bark_icon)

    print('finish')


if __name__ == '__main__':
    main()
