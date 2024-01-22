import json
import os
import random
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


def sign(token, bark_deviceKey, bark_icon):
    if not token:
        token = ''

    if len(token) > 0:
        print('有token，需要执行签到')

        url = 'https://link-ai.tech/api/chat/web/app/user/sign/in'
        headers = {
            'Authorization': 'Bearer ' + token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.post(url, headers=headers)

        print(response.text)

        title = 'Link.AI-签到结果'
        message = ''

        if "success" in response.text:
            message = '成功签到'
        elif "今日已签到" in response.text:
            message = '今日已签到，请明日再来！'
        elif "401" in response.text:
            message = 'jwt校验失败，请检查'
        else:
            message = '签到结果解析错误'

        bark(bark_deviceKey, title, message, bark_icon)

    else:
        print('不执行签到')


def main():
    bark_device_key = os.environ.get('BARK_DEVICEKEY')
    bark_icon = os.environ.get('BARK_ICON')

    wait = random.randint(3, 110)
    time.sleep(wait)

    authorization = os.environ.get('Authorization')
    sign(authorization, bark_device_key, bark_icon)

    print('finish')


if __name__ == '__main__':
    main()
