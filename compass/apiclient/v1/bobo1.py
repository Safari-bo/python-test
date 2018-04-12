import requests
import json
import sys
import io

url_root = "192.168.76.91"

# data used to login
login_data = {"email": "admin@fiberhome.com",
        "password": "admin",
        "remember": "false"
        }
s
# set request head
headers = {"User-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
           "Accept": "application/json,text/plain,*/*",
           "Cookie": "remember_token=$1$vwZ2ALbY$aD0S5KaEqMU9P42c7LnPZ0;session=.eJxNjrFugzAURX-l8pzBOMmClKGSgRT1GZnYRH5LpARa-owXUkRxlH8v3aqru1zpXJ0Hu3yM3b1n6fc4dRt2-WpZ-mAvV5YyVTiBlHs0N66K2gNpjgaDi9kOgkucqAcl24BnPYOABIo6wLkmNGsJogolVRKDMk0PUs9K4ABkI5KfIdikkkOAoGcXFalod1Wh100LlJ6DdBGNW5m3n0rmvjJl76LmKugEyS5Ir1s0lkNcQ9mBPTdsunfjf_9SZv7K9wtsb1PNucdtjiehGjjm-yb7c8xtk5X2FNvl_fOwfjx_ATGsWFY.DaSE1Q.iRJXckr0_AtdjerpGOB8vVADHB4"}

# Init session
session = requests.Session()
session.headers.update(headers)

# #login url
# login_url = 'http://{}/api/users/login'.format(url_root)
# # use session to send login request,then store cookie in session,
# # use print(session.cookies.get_dict())
# resp = session.post(login_url, json.dumps(login_data))
# # print type(resp.content)
# print session.headers
# print resp.content
# print type(resp.cookies)
# print type(resp.cookies.get_dict())
# print resp.cookies
# print type(resp.headers)
# print resp.headers.keys()

# request cluster state
cluster_state_url = 'http://{}/api/clusters/1/state'.format(url_root)
print session.headers
resp = session.get(cluster_state_url)
# print type(resp.content)
print(resp.content.decode('utf-8'))
print resp.headers