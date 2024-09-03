import util
mac = util.get_local_mac()
mac = mac.replace(":","")
key = mac
##port
serve_port = 8000
##API
api_host = "http://81.70.52.233/api/aiot/"
key = "112233445566" #注释掉本行获取本机mac地址作为key
secret = key+"AIoT!@#123"
##SSH
ssh_username = "user"
ssh_password = "password"
