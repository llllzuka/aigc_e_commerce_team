import ssl
import requests

print("SSL Version:", ssl.OPENSSL_VERSION)
print("Requests Version:", requests.__version__)

# 尝试访问一个 HTTPS 网站
try:
    response = requests.get("https://httpbin.org/get")
    print("HTTPS 请求成功！状态码:", response.status_code)
except Exception as e:
    print("HTTPS 请求失败:", e)