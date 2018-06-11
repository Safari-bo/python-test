import subprocess
import os
import sys
import ConfigParser
import threading
import re
import commands
import csv

lock = threading.Lock()

cmd1 = "ansible -i /var/lib/fitdep/playbooks/hosts_all optimize_nodes -m shell -a 'modprobe ipmi_msghandler;modprobe ipmi_devintf;modprobe ipmi_si;modprobe ipmi_poweroff;modprobe ipmi_watchdog'"
p1 = subprocess.Popen(cmd1, shell=True, stdout=subprocess.PIPE)
p1.wait()
if p1.returncode != 0:
    print "errors encounter"
    for line in p1.stdout.readlines():
        print line,
    sys.exit(1)

ip_dict = {}
ip_list = []
conf = ConfigParser.ConfigParser()
conf.read('/var/lib/fitdep/playbooks/hosts_all')
for entry in conf.options('optimize_nodes'):
    ip_dict[entry.split(' ')[0]] = {}
print ip_dict.keys()


def execute_cmd(ip):
    ent = {"hostname": "host",
             "pxe": "127.0.0.1",
             "mgnt": "127.0.0.1",
             "ipmi": "127.0.0.1",
             "sn": "0123456789"}
    cmd = "ssh root@" + ip + " 'cat /etc/hostname'"
    ent['hostname'] = commands.getoutput(cmd).split('\r\n')[-1]
    cmd = "ssh root@" + ip + " 'ip addr show brpxe'"
    pxe = commands.getoutput(cmd)
    if re.search('inet ((\d{1,3}\.){3}(\d{1,3}))', pxe) != None:
        ent['pxe'] = re.search('inet ((\d{1,3}\.){3}(\d{1,3}))', pxe).group(1)
    cmd = "ssh root@" + ip + " 'ip addr show mgnt'"
    mgnt = commands.getoutput(cmd)
    if re.search('inet ((\d{1,3}\.){3}(\d{1,3}))', mgnt) != None:
        ent['mgnt'] = re.search('inet ((\d{1,3}\.){3}(\d{1,3}))', mgnt).group(1)
    cmd = "ssh root@" + ip + " 'ipmitool lan print 1'"
    ipmi = commands.getoutput(cmd)
    if re.search('IP Address.*: ((\d{1,3}\.){3}(\d{1,3}))', ipmi) != None:
        ent['ipmi'] = re.search('IP Address.*: ((\d{1,3}\.){3}(\d{1,3}))', ipmi).group(1)
    cmd = "ssh root@" + ip + " 'ipmitool fru'"
    sn = commands.getoutput(cmd)
    if re.search('Product Serial.*: (\w.*)', sn) != None:
        ent['sn'] = re.search('Product Serial.*: (\w.*)', sn).group(1)
    if lock.acquire():
        # ip_list.append(ent)
        ip_dict[ip] = ent
        lock.release()

threads = []
for ip in ip_dict.keys():
    threads.append(threading.Thread(target=execute_cmd, args=(ip,)))
for td in threads:
    td.start()
for td in threads:
    td.join()

# print ip_dict

with open('./ip_dict.csv', 'w') as f:
    header = ['Name', 'IPMI_IP', 'PXE_IP', 'Mgnt_IP', 'SN']
    file_writer = csv.writer(f)
    file_writer.writerow(header)
    for host in sorted(ip_dict.keys()):
        entry = [ip_dict[host]['hostname'], ip_dict[host]['ipmi'], ip_dict[host]['pxe'], ip_dict[host]['mgnt'], ip_dict[host]['sn']]
        file_writer.writerow(entry)
