import sys
import requests
from datetime import datetime
from hashlib import md5
import base64


server = 'http://127.0.0.1:8000'

# server host
server = 'http://81.70.52.233'


'''
api测试

usage: python apitest.py args
命令行执行：python apitest.py 接口 参数

1. 生成签名
python apitest.py sign
sign:  c8687cbe76b53009105f7a90a55e744a1122334455661723741933

2. 验证签名
python apitest.py checksign c8687cbe76b53009105f7a90a55e744a1122334455661723741933
sign:  c8687cbe76b53009105f7a90a55e744a1122334455661723741933
sign info:  {'timestamp': '1723741933', 'key': '112233445566', 'secret': 'c8687cbe76b53009105f7a90a55e744a'}
sign mac:  11:22:33:44:55:66

3. 获取消息
python apitest.py task
url: http://127.0.0.1:8000/api/aiot/task?sign=b9e03a28f5101b3a365296ef628825e81122334455661723742145
params: None
response: {'code': 200, 'message': 'success', 'data': {'tasks': []}}

4.状态上报
python apitest.py status
url: http://127.0.0.1:8000/api/aiot/status?sign=05259eca762dae79fc8bb71f0d4207781122334455661723742186
params: {'ip': '192.168.0.10', 'cameras': [{'camera': '11:22:33:44:55:77', 'ip': '192.168.0.11', 'status': 1}, {'camera': '11:22:33:44:55:88', 'ip': '192.168.0.12', 'status': 1}]}
response: {'code': 200, 'message': 'success', 'data': {'timestamp': 1723742186, 'timezone': '+08:00'}}

5.事件上报
python apitest.py event
url: http://127.0.0.1:8000/api/aiot/event?sign=613f09615f55d3050e2fc652592cce1e1122334455661723742223
params: {'events': [{'camera': '11:22:33:44:55:77', 'area': 'all', 'event': '1001', 'timestamp': 1723742223, 'image': 'data:image/jpeg;base...'}]}
response: {'code': 200, 'message': 'success', 'data': {'id': 35, 'uid': 0, 'cid': 1, 'type': 1001, 'status': 1, 'place': 1, 'area': 2, 'image': '2024/08/16/abc922ecf7724c06914eefc1c741650f.jpg', 'create_time': '2024-08-16 01:17:03', 'update_time': '2024-08-16 01:16:08'}}

'''


def create_sign(timestamp: str, key: str, secret: str):
    sign_data = f"{key}{timestamp}{secret}"
    sign = md5(sign_data.encode()).hexdigest()
    return f"{sign}{key}{timestamp}"

def check_sign(sign: str):
    data = {}
    if not sign or len(sign) != 54:
       return data
    data['timestamp'] = sign[-10:]
    data['key'] = sign[32:-10]
    data['secret'] = sign[0:32]
    return data



def api_test(api_key, api_args=None):

    api_prefix = '/api/aiot/'
    api_url = server + api_prefix

    if api_key == "":
        return False
    
    if api_key == "sign":

        #1.鉴权参数
        mac = '11:22:33:44:55:66'
        key = mac.replace(':', '') #设备编号，设备MAC小写去冒号，12位字符
        secret = key+"AIoT!@#123" #设备秘钥，默认为设备编号去冒号+AIoT!@#123
        timestamp = str(int(datetime.now().timestamp())) #请求时间，调用接口时的秒级时间，10位字符
        sign = create_sign(timestamp, key, secret)

        print('sign: ', sign)
    
        return True
    
    if api_key == "checksign":
        if api_args:
            sign = api_args
        else:
            mac = '11:22:33:44:55:66'
            key = mac.replace(':', '') #设备编号，设备MAC小写去冒号，12位字符
            secret = key+"AIoT!@#123" #设备秘钥，默认为设备编号去冒号+AIoT!@#123
            timestamp = str(int(datetime.now().timestamp())) #请求时间，调用接口时的秒级时间，10位字符
            sign = create_sign(timestamp, key, secret)
        
        print('sign: ', sign)
        data = check_sign(sign)
        print('sign info: ', data)
        if data.get('key'):
            mac = ":".join(data['key'][i:i+2] for i in range(0, len(data['key']), 2))
            print('sign mac: ', mac)
        else:
            print('sign error')
        return True
    
    else:

        # 签名
        mac = '11:22:33:44:55:66'
        key = mac.replace(':', '') #设备编号，设备MAC小写去冒号，12位字符
        secret = key+"AIoT!@#123" #设备秘钥，默认为设备编号去冒号+AIoT!@#123
        timestamp = str(int(datetime.now().timestamp())) #请求时间，调用接口时的秒级时间，10位字符
        sign = create_sign(timestamp, key, secret)

        # 获取消息
        if api_key == "task":
            response = requests.post(api_url+'task', params={'sign': sign})
            print('url:', api_url+api_key+'?sign='+sign)
            print('params:', None)
            print('response:', response.json())
            return True
        
        # 状态上报
        if api_key == "status":
            data = {}
            data['ip'] = '192.168.0.10'
            data['cameras'] = []
            data['cameras'].append({'camera': '11:22:33:44:55:77', 'ip': '192.168.0.11', 'status': 1})
            data['cameras'].append({'camera': '11:22:33:44:55:88', 'ip': '192.168.0.12', 'status': 1})
            response = requests.post(api_url+api_key, params={'sign': sign}, json=data)
            print('url:', api_url+api_key+'?sign='+sign)
            print('params:', data)
            print('response:', response.json())
            return True
        
        # 事件上报
        if api_key == "event":

            image_url = 'https://image.cqrb.cn/d/file/news/image/uploadImage/2021-10-15/469186168e535dba6f.jpg'
            image_content = requests.get(image_url).content
            base64_image_content = base64.b64encode(image_content).decode('utf-8')
            base64_image = f'data:image/jpeg;base64,{base64_image_content}'

            data = {}
            data['events'] = []

            event = {}
            event['camera'] = '11:22:33:44:55:77'
            event['area'] = 'all'
            event['event'] = '1001'
            event['timestamp'] = int(datetime.now().timestamp())
            # event['timestamp'] = 1723740233
            event['image'] = base64_image
            data['events'].append(event)

            req = requests.Request("post",api_url+api_key, params={'sign': sign}, json=data)
            prepped = req.prepare()

            print('url:', api_url+api_key+'?sign='+sign)
            
            event['image'] = base64_image[0:20]+'...'
            data = {}
            data['events'] = [event]
            print('params:', data)

            # print('response:', response.text)
            print('response:', response.json())
            return True

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("usage: python apitest.py args", sys.argv)
        sys.exit(1)

    api_key = sys.argv[1]
    api_args = None
    if len(sys.argv) == 3:
        api_args = sys.argv[2]
    
    api_test(api_key, api_args)