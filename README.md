# 如何使用？ 
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
