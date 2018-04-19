import sys

def test1(func):
    def inner(func):
        response = func()
        if response['status'] >= 400:
            print response
            sys.exit(1)
        else:
            return func
    return inner()

@test1
def test2(response):
    return response

resp1 = {'status': 400, 'result': 'Test failed'}
resp2 = {'status': 200, 'result': 'Test success'}

print test2(resp1)
print test2(resp2)