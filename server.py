from socket import *
import email
import sys

host = "127.0.0.1"
port = 9999

table = {
    "Doldol" : { "type" : "chicken", "age" : 1, "leg" : 2 },
    "Baduk" : { "type" : "dog", "age" : 3, "leg" : 4 },
    "Yaong" : { "type" : "cat", "age" : 2, "leg" : 4 }
}

# httpHeader = f"GET / HTTP/1.1\r\nContent-Type: {}\r\nContent-Length: {}\r\n\n"
# responseMessage = f"HTTP/1.1 {status} {statusMessage}\r\nContent-Type: {}\r\nContent-Length: {}\r\n\n" 
def makeResponseMessage(message):
    index = message.find("{")
    requestBody = message[index:]
    firstHeader, headers = message[:index].split("\r\n", 1)
    message = email.message_from_string(headers)
    headers = dict(message.items())

    (method, directory, _) = firstHeader.split()
    status = 200
    statusMessage = "OK"
    responseBody = ""
    if (method == "GET"):
        responseBody = str(table[directory[1:]])
    elif (method == "HEAD"):
        responseBody = ""
    elif (method == "POST"):
        table.update(eval(requestBody))
        responseBody = str(table[directory[1:]])
        status = 201
        statusMessage = "Created"
    elif (method == "PUT"):
        table.update(eval(requestBody))
        responseBody = str(table[directory[1:]])
    bodySize = len(responseBody)
    responseMessage = f"HTTP/1.1 {status} {statusMessage}\r\nContent-Type: application/json\r\nContent-Length: {bodySize}\r\n\n"
    responseMessage += responseBody

    print("responseMessage: " + responseMessage)
    return responseMessage


#init

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, port))
serverSocket.listen(1)
print("Server: listening...")

connectionSocket, clientAddress = serverSocket.accept()
while True:

    print(f"Connected from {str(clientAddress)}")
    data = connectionSocket.recv(1024)
    requestMessage = data.decode("utf-8")
    print(f"Received message: {requestMessage}")

    connectionSocket.send(makeResponseMessage(requestMessage).encode("utf-8"))

    serverSocket.close()




# 1. bind
# 2. listen
# while 문
# accept
