import json
from copy import deepcopy
from Cheetah.Template import Template

with open('../config_dict.json', 'r') as f:
    cluster_conf_data = json.load(f)

searchList = []
copy_vars_dict = deepcopy(cluster_conf_data)
for key, value in cluster_conf_data.iteritems():
    if isinstance(value, dict):
        temp = copy_vars_dict[key]
        del copy_vars_dict[key]
        searchList.append(temp)
searchList.append(copy_vars_dict)

tmpl = Template(file=open("./deploy2.cfg", "r"), searchList=searchList)
print tmpl.respond()