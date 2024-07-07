from socket import *
import sys

ip = "127.0.0.1"
port = 9999

# request message를 만들어 return하는 함수
def makeRequestMessage(userInput):
    # 잘못된 input 처리
    if (len(userInput.split()) != 2):
        return -1
    # get a -> method = get, name = a
    method, name = userInput.split()
    method = method.upper()
    responseBody = ""
    if (method == "GET"):
        # 모든 data를 요청할 경우 path를 "/"로 설정하기 위해 name을 ""로 설정한다
        if (name.upper() == "ALL"):
            name = ""
    elif (method == "HEAD"):
        pass
    elif (method == "POST" or method == "PUT"):
        # 추가/수정할 데이터 입력을 요청한다
        print("Enter information: [type] [age] [leg]")
        userInput = sys.stdin.readline().strip().split()
        # 잘못된 input 처리
        if (len(userInput) != 3):
            return -1
        # reponse body는 application/json 형태로 구성한다
        responseBody = str({ name : { "type": userInput[0], "age": userInput[1], "leg": userInput[2]}})

    # request message를 구성하여 return한다
    path = "/" + name
    contentType = "application/json"
    contentLength = len(responseBody)
    httpHeader = f"{method} {path} HTTP/1.1\r\nContent-Type: {contentType}\r\nContent-Length: {contentLength}\r\n\n"
    return httpHeader + responseBody
    
# IPv4 주소를 사용하고 TCP 통신을 한다.
clientSocket = socket(AF_INET, SOCK_STREAM)
# server의 ip, port 주소로 접속한다
clientSocket.connect((ip, port))
# httpHeader = f"GET / HTTP/1.1\r\nContent-Type: {}\r\nContent-Length: {}\r\n\n"

# request response를 주고 받는 while문
while True:

    # 사용자로부터 input을 받는다
    print("Enter: [method] [objectName]")
    userInput = sys.stdin.readline().strip()

    # q를 입력할 경우 while문 실행 종료
    if (userInput == "q"):
        break
    
    # request message를 생성한다
    requestMessage = makeRequestMessage(userInput)
    # 잘못된 input 처리
    if (requestMessage == -1):
        print("Wrong Input: try again")
        continue
    
    # request message를 server에 전송한다
    clientSocket.send(requestMessage.encode("utf-8"))

    # server로부터 response message를 받는다
    data = clientSocket.recv(1024)
    responseMessage = data.decode("utf-8")
    
    print("----------RESPONSE------------\n")
    print(responseMessage)
    print("------------------------------\n")


# clinet를 종료한다
clientSocket.close()