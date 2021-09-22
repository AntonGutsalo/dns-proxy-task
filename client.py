import socket
import config

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((config.IP, int(config.PORT)))
client_request = input()
client.send(client_request.encode("UTF-8"))
get_server = client.recv(1024).decode('UTF-8')
print(get_server)
