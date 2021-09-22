import json
import socket
import requests
import config

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', int(config.PORT)))
server.listen()


def open_socket():
    while True:
        client, address = server.accept()
        request = client.recv(1024).decode('UTF-8')
        answer = check_black_list(request)
        if answer == 1:
            client.send("domain name in BlackList".encode())
        else:
            request_ip = server_dns(request)
            if request_ip == 0:
                client.send("It`s unreal domain name".encode())
            else:
                server_answer = requests.get('http://' + request_ip)
                if server_answer.status_code == 200:
                    client.send("Your domain's name ip: ".encode() + request_ip.encode())
                else:
                    client.send("Unable to access site at this time".encode())


def check_black_list(domain):
    with open('BlackList', "r") as file:
        json_blacklist = json.load(file)
        if domain in json_blacklist["black_list"]:
            return 1
        else:
            return 0


def server_dns(domain):
    with open('DnsServer', "r") as file:
        json_dns = json.load(file)
    if domain not in json_dns["dns_list"]:
        return 0
    ip = json_dns["dns_list"][domain]
    return ip


if __name__ == '__main__':
    open_socket()
