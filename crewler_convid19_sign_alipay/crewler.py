import requests, json, random
from faker import Faker

f=Faker(locale="zh_CN")
student_id=int(input('学号/工号: '))
student_name=str(input('姓名: '))
request_data = {
    'schoolNo': 4136010406,  #昌航的学校代码
    'xhOrZgh': student_id,   #学号
    'sfzMd5': random.randint(1,999),       #随便填
    'cardId': random.randint(1,999),       #随便填
    'xm': '',           #不用填
    'loginXm': student_name, #姓名
}

headers = {
    'Accept': '*/*',
    'User-agent': f.user_agent(),
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}
print('获取中...')
res = requests.post('https://xycr.jx.edu.cn/public/registerSchool', headers=headers, data=request_data)

# cookies = res.cookies
# headers = res.headers
if res.status_code!=200:
    print('请求失败')
else:
    json = json.loads(res.text)
    if json['code']==1001:
        signed_url = json['data'] ##签到的链接
        #print(data)

        res1 = requests.get(signed_url, allow_redirects=False)
        # headers = res.headers
        #
        # print(headers)
        cookies=res1.cookies.get_dict()
        #print(cookies)
        print('个人疫情签到首页: '+signed_url)
        print('身份证后6位: '+cookies['yzxx'])#身份证后6位
        print('校园网初始密码: Nchu'+cookies['yzxx'])#初始密码
    else:
        print(json['msg'])

