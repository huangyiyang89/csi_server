from tests.test_main import client

# 测试登录成功
def test_login_success():
    # 模拟请求数据
    request_data = {
        "username": "admin",
        "password": "admin"
    }
    # 执行登录方法
    response = client.post("/api/users/login", json=request_data)
    # 断言登录成功的响应
    assert response.json() == {"message": "登录成功"} and response.status_code == 200


# 测试登录失败
def test_login_failure():
    # 模拟请求数据
    request_data = {
        "username": "admin",
        "password": "wrong_password"
    }
    # 执行登录方法
    response = client.post("/api/users/login", json=request_data)
    # 断言登录失败的响应
    assert response.json() == {"detail": "用户名或密码错误"} and response.status_code == 401