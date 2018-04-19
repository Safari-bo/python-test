import sys

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
def func1(response):
    return response

resp1 = {'status': 400, 'result': 'Test failed'}
resp2 = {'status': 200, 'result': 'Test success'}


print func1(resp1)
print func1(resp2)