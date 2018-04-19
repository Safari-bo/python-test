import requests
import json
import sys
import time


# data
login_data = {"email": "admin@fiberhome.com",
        "password": "admin",
        "remember": "false"
        }

cluster_init_data = {"adapter_id": "openstack_newton",
                     "flavor_id": "openstack_newton:HA-ansible-multinodes-newton",
                     "name": "new_cluster",
                     "os_id": "CentOS-7-fh-x86_64"
                    }

with open('../import_cluster.json', 'r') as f:
    cluster_conf_data = {"import_cluster": json.load(f)}

# set request head
headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
           'Content-Type': 'application/json;charset=utf-8'}

url_root = "10.127.2.12:8080"
login_url = 'http://{}/api/users/login'.format(url_root)
cluster_list_url = 'http://{}/api/clusters'.format(url_root)
cluster_add_url = "http://{}/api/clusters".format(url_root)


def wrapper(func):
    def inner(*args, **kwargs):
        response = func(*args, **kwargs)
        if response['status'] >= 400:
            print response
            sys.exit(1)
        else:
            return response
    return inner


@wrapper
def get_cluster_number(_session, url=cluster_list_url):
    response = _session.get(url)
    return {'status': response.status_code,
            'result': len(response.json())}


@wrapper
def get_cluster_id(_session, url=cluster_list_url):
    response = _session.get(url)
    return {'status': response.status_code,
            'result': response.json()[0]['id']}


@wrapper
def login(_session, url=login_url, data=login_data):
    response = _session.post(url, json.dumps(data))
    return {'status': response.status_code,
            'result': response.json()}


@wrapper
def add_cluster(_session, url=cluster_add_url, data=cluster_init_data):
    response = _session.post(url, json.dumps(data))
    return {'status': response.status_code,
            'result': response.json()}


@wrapper
def get_cluster_state(_session, id=1):
    cluster_state_url = 'http://{}/api/clusters/{}/state'.format(url_root, id)
    response = _session.get(cluster_state_url)
    return {'status': response.status_code,
            'result': response.json()}


@wrapper
def import_cluster_config(_session, id=1, data=cluster_conf_data):
    cluster_import_url = 'http://{}/api/clusters/{}/action'.format(url_root, id)
    response = _session.post(cluster_import_url, json.dumps(data))
    return {'status': response.status_code,
            'result': response.json()}


@wrapper
def review_cluster(_session, id=1):
    cluster_review_url = 'http://{}/api/clusters/{}/action'.format(url_root, id)
    host_num = get_cluster_state(_session)['result']['status']['total_hosts']
    data = {"review":
                {"hosts": [i+1 for i in range(host_num)]}
            }
    response = _session.post(cluster_review_url, json.dumps(data))
    return {'status': response.status_code,
            'result': response.json()}


@wrapper
def deploy_cluster(_session, id=1):
    cluster_deploy_url = 'http://{}/api/clusters/{}/action'.format(url_root, id)
    host_num = get_cluster_state(_session)['result']['status']['total_hosts']
    data = {"deploy":
                {"hosts": [i+1 for i in range(host_num)]}
            }
    response = _session.post(cluster_deploy_url, json.dumps(data))
    return {'status': response.status_code,
            'result': response.json()}

if __name__ == '__main__':
    session = requests.session()
    print login(session)
    while get_cluster_number(session)['result'] == 0:
        print add_cluster(session)
        time.sleep(5)
    print get_cluster_state(session)
    print import_cluster_config(session)
    time.sleep(5)
    print get_cluster_state(session)
    print review_cluster(session)
    print deploy_cluster(session)