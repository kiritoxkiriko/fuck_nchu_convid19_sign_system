import requests, json, random, os,sys
from faker import Faker

f = Faker(locale="zh_CN")
headers = {
    'Accept': '*/*',
    'User-agent': f.user_agent(),
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

KEY = 'SCU21273Td787772b5aad3e2590a887408006164e5a744d174e51c' #填自己的SCKEY


def get_user_URL(user_id: int, user_name: str):
    request_data = {
        'schoolNo': 4136010406,  # 昌航的学校代码
        'xhOrZgh': user_id,  # 学号
        'sfzMd5': random.randint(1, 999),  # 随便填
        'cardId': random.randint(1, 999),  # 随便填
        'xm': '',  # 不用填
        'loginXm': user_name,  # 姓名
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
    if res.status_code != 200:
        print('请求失败')
        return ""
    else:
        res_json = json.loads(res.text)
        if res_json['code'] == 1001:
            signed_url = res_json['data']  ##签到的链接
            print(signed_url)
            return signed_url
        else:
            print(res_json['msg'])
            return ""


def get_session_by_user_URL(user_URL):
    session = requests.session()
    res = session.get(user_URL, allow_redirects=False, headers=headers)
    cookies = res.cookies.get_dict()
    session_id = cookies['JSESSIONID']
    return session


def submit_dcwj_by_session(session, name, class_id, year, faculty, address) -> bool:
    requests_data = {
        'dcwj': json.dumps({
            'name': name,
            'xb': '0',
            'gtjzrysfyyshqzbl': 'N',
            'xzzdsfyyqfbqy': 'N',
            'jqsfqwzdyq': 'N',
            'sfzyblbbdsq': 'N',
            'sfyhqzbljcs': 'N',
            'sfszsqjfjcxqz': 'N',
            'jrtw': '36.5',
            'xcwz': '2',
            'sf': '0',
            'stype': '0',
            'xy': faculty,
            'nj': year,
            'bj': class_id,
            'age': '',
            'lxdh': '',
            'jjdh': '',
            'sfz': '',
            'szd': '1',
            'address': address,
            'hbc': '',
            'hjtgj': '3',
            'sffx': '1',
            'jkzk': '0',
        }),
    }

    res = session.post('https://fxgl.jx.edu.cn/4136010406/dcwjEditNew/dcwjSubmit2', data=requests_data, headers=headers)
    result = json.loads(res.text)  # 解析返回的数据
    if int(result['code']) == 1001:
        print("提交问卷成功")
        return True, ''
    else:
        print("提交问卷失败")
        print(result['msg'])
        return False, result['msg']


def sign_by_session(session) -> bool:
    requests_data = {
        'province': '天津市', ##签到地址可自己替换，也可使用faker随机生成
        'city': '天津市',
        'district': '河北区',
        'street': '民生路',
        'xszt': 0,
        'jkzk': 0,
        'jkzkxq': '',
        'sfgl': 1,
        'gldd': '',
        'mqtw': 0,
        'mqtwxq': '',
        'zddlwz': '天津市天津市河北区',
        'sddlwz': '',
        'bprovince': '天津市',
        'bcity': '天津市',
        'bdistrict': '河北区',
        'bstreet': '民生路',
        'sprovince': '天津市',
        'scity': '天津市',
        'sdistrict': '河北区',
        'lng': '117.21081309',
        'lat': '39.1439299',
        'sfby': 1,
    }
    res = session.post('https://fxgl.jx.edu.cn/4136010406/studentQd/saveStu', data=requests_data, headers=headers)

    if res.status_code == 200:
        print("签到成功")
        return True
    else:
        print("签到失败")
        return False


def auto_sign(student_id, name, faculty) -> dict:
    result = {
        'id': student_id,
        'name': name,
        'isSign': '',
        'isSubmit': '',
        'msg': '',
    }
    year = '20' + student_id[0:2]
    class_id = student_id[0:6]
    address = f.address()

    print(student_id, name)

    user_URL = get_user_URL(student_id, name)
    session = get_session_by_user_URL(user_URL)
    isSign = sign_by_session(session)
    submit_result = submit_dcwj_by_session(session, name, class_id, year, faculty, address)
    return {
        'id': student_id,
        'name': name,
        'isSign': isSign,
        'isSubmit': submit_result[0],
        'msg': submit_result[1],
    }


def push_msg_to_wechat(title: str, msg: str):
    request_data = {
        'text': title,
        'desp': msg,
    }
    res = requests.post('https://sc.ftqq.com/' + KEY + '.send', request_data)
    if res.status_code == 200:
        print('推送 ' + title + ' 成功')
        return True
    else:
        print('推送 ' + title + ' 失败')
        return False


def read_users(file_name):
    users = []
    lines = []
    with open(sys.path[0]+'/'+file_name, mode='r', encoding='utf-8') as f:
        lines = f.readlines()

    for s in lines:
        users.append(s.split(','))

    return users


if __name__ == '__main__':
    users = read_users('data.txt')
    results = []
    for i in users:
        results.append(auto_sign(i[0], i[1], i[2]))
    title = '疫情系统自动签到状态'

    str = ''

    for i in results:
        str += i['id'] + '-' + i['name'] + ' 签到状态:' + ('成功' if i['isSign'] else '失败') + ' 问卷状态:' + (
            '成功' if i['isSubmit'] else i['msg']) + '\n'

    push_msg_to_wechat(title, str)
