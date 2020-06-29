import requests
import sys
import json

URL = "http://localhost:1337/"

command = sys.argv[1:]
if command[0] == 'transfer':
    if(len(command) == 6 and command[2] == 'from' and command[4] == 'to'):
        try:
            data = {
                'from': command[3],
                'to': command[5],
                'amount': float(command[1])
            }
            res = requests.post(URL + 'transfer', data=data)
            print(res.text)
        except ValueError:
            print("amount should be number!")
    else:
        print('Invalid commands!')
        print('Usage: transfer <amount> from <src> to <dst>')
elif command[0] == 'get':
    getCmdList = ["timestamp", "head"]
    if(len(command) == 2 and command[1] in getCmdList):
        res = requests.get(URL + command[1])

        try:
            text = json.loads(res.text)
            print(json.dumps(text, indent=2))
        except BaseException:
            print(res.text)
    else:
        print('Invalid commands!')
        print('Usage: get timestamp / get head')
