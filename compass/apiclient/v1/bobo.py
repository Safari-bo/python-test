

import requests
import json
import sys
import io



url_root = "10.127.2.12:8080"

# data used to login
login_data = {"email": "admin@fiberhome.com",
        "password": "admin",
        "remember": "false"
        }

cluster_init_data = {"adapter_id": "openstack_pike",
                     "flavor_id": "openstack_pike:HA-ansible-multinodes-pike",
                     "name": "test",
                     "os_id": "CentOS-7-fh-x86_64"
                    }

with open('../import_cluster.json', 'r') as f:
    cluster_conf_data = {"import_cluster": json.load(f)}
    print cluster_conf_data.keys()

# set request head
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
           'Content-Type': 'application/json;charset=utf-8'}

# Init session
session = requests.Session()

#login url
login_url = 'http://{}/api/users/login'.format(url_root)
# use session to send login request,then store cookie in session,
# use print(session.cookies.get_dict())
resp = session.post(login_url, json.dumps(login_data))
# print type(resp.content)
print resp.content

# request cluster state
cluster_state_url = 'http://{}/api/clusters/1/state'.format(url_root)
resp = session.get(cluster_state_url)
# print type(resp.content)
print(resp.content.decode('utf-8'))

# add a new cluster
cluster_add_url = "http://{}/api/clusters".format(url_root)
resp = session.post(cluster_add_url, json.dumps(cluster_init_data))
# print resp.content

# import cluster configuration data
cluster_import_url = "http://{}/api/clusters/1/action".format(url_root)
resp = session.post(cluster_import_url, json.dumps(cluster_conf_data))
print resp.content

# review cluster before deploy
cluster_review_url = cluster_import_url
resp = session.post(cluster_review_url, json.dumps({"review":{"hosts":[1, 2, 3]}}))
print resp.content

# deploy cluster
cluster_deploy_url = cluster_import_url
resp = session.post(cluster_deploy_url, json.dumps({"deploy":{"hosts":[1, 2, 3]}}))
print resp.content