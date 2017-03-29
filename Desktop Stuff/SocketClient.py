import socket

host="136.227.162.110"
port=5060

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((host,port))

while True:
    command=input("enter command")
    if commoand=='EXIT':
        s.send(str.encode(command))
        break
    elif command=="KILL":
        s.send(str.encode(comand))
        break
    s.send(str.encode(command))
    reply=s.recv(1024)
    print(reply.decode('utf-8'))

s.close()
