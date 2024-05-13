# 如何使用？ 

0、前言

2024年5月13日10:15:58

取Authorization值做了验证，null、空、错误值都会直接结束，不会走到后面的jwt解析逻辑。

若只是暂时不需要执行签到，而不想删除仓库，可以将Authorization的值填个 "1"，这样会直接结束。

2024年3月19日08:43:15

目前我是使用微信扫码登录的，获取的Authorization的值有效期只有7天。

1、Fork项目到自己的仓库

2、点击Settings -> 点击选项卡 Secrets and variables -> 点击Actions -> New repository secret

(1)目前预设1个

(2)关于Bark推送，不用的话填空即可


    | Name   | Secret                           |
    | ------ | ------------------------------- |
    | Authorization  | Authorization的值 |
    | BARK_DEVICEKEY  | IOS应用Bark 推送密钥 |
    | BARK_ICON  | IOS应用Bark 推送的图标 |

3、点击Actions -> 选择linkai-sign -> 点击Run workflow 运行即可

4、关于签到的定时时间

linkaisign.yml，调整 \- cron: 20 21 * * *，对应北京时间5:20
