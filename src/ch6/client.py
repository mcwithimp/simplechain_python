import sys


print(sys.argv)
print(' '.join(sys.argv[1:]))

command = sys.argv[1]
if command == 'transfer':
    pass
elif command == 'get':
    target = sys.argv[2]
