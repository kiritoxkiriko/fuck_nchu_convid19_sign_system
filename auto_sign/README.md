# 说明
* 按格式将学生数据放入同目录下data.txt即可  
每行格式为 **学号, 姓名, 学院, 省份，城市，区，街道，经度，纬度**  
按行分隔每个数据
* auto_sign.py 中KEY的值填 server酱 的 SCKEY, 可将签到状态推送至微信   
api申请网址: [server酱](http://sc.ftqq.com/3.version)
* 先使用 ```pip3 install -r requirements.txt``` 安装依赖包  
运行 ```python3 auto_sign.py``` 即可签到  
* 可配合crontab实现自动签到
