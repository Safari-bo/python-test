from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('jinja.cfg')
print template.render(test=['192.168.122.11', '192.168.122.12', '192.168.122.13'])