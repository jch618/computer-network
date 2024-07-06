from socket import *
import sys

ip = "127.0.0.1"
port = 9999

def makeRequestMessage(userInput):
    method, name = userInput.split()
    method = method.upper()
    responseBody = ""
    if (method == "GET"):
        pass
    elif (method == "HEAD"):
        pass
    elif (method == "POST" or method == "PUT"):
        print("Enter information: [type] [age] [leg]")
        userInput = sys.stdin.readline().strip().split()
        responseBody = str({ name : { "type": userInput[0], "age": userInput[1], "leg": userInput[2]}})

    directory = "/" + name
    contentType = "application/json"
    contentLength = len(responseBody)
    httpHeader = f"{method} {directory} HTTP/1.1\r\nContent-Type: {contentType}\r\nContent-Length: {contentLength}\r\n\n"
    return httpHeader + responseBody
    

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((ip, port))
print("connect ok")
# httpHeader = f"GET / HTTP/1.1\r\nContent-Type: {}\r\nContent-Length: {}\r\n\n"

# send request
while True:

    print("Enter: [method] [objectName]")
    userInput = sys.stdin.readline().strip()
    if (userInput == "q"):
        break
    clientSocket.send(makeRequestMessage(userInput).encode("utf-8"))

    data = clientSocket.recv(1024)
    responseMessage = data.decode("utf-8")
    print("data:\n" + responseMessage)

clientSocket.close()