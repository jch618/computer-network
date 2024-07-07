from socket import *

#host = "192.168.0.15"
host = "127.0.0.1"
port = 9999

# data table
table = {
    "Doldol" : { "type" : "chicken", "age" : 1, "leg" : 2 },
    "Baduk" : { "type" : "dog", "age" : 3, "leg" : 4 },
    "Yaong" : { "type" : "cat", "age" : 2, "leg" : 4 }
}

# request message format: f"GET / HTTP/1.1\r\nContent-Type: {}\r\nContent-Length: {}\r\n\n"
# response message format = f"HTTP/1.1 {status} {statusMessage}\r\nContent-Type: {}\r\nContent-Length: {}\r\n\n" 

# http 상태 코드가 500일 때 처리
def handleStatus500():
    status = 500
    statusMessage = "Internal Server Error"
    return (status, statusMessage)

# http 상태 코드가 204일 때 처리
def handleStatus204():
    status = 204
    statusMessage = "No Content"
    return (status, statusMessage)

def handleStatus201():
    status = 201
    statusMessage = "Created"
    return (status, statusMessage)

# request message의 요청에 따라 알맞은 response message를 생성해 return하는 함수
def makeResponseMessage(message):
    # request message에서 Content type을 application/json으로 설정하였기 때문에
    # body는 { "a" : "value1", "b" : "value2" } 꼴이다
    index = message.find("{")
    requestBody = message[index:]

    # firstHeader는 header의 첫 line이다 ex) GET / HTTP/1.1
    firstHeader = message[:index].split("\r\n", 1)[0]

    (method, path, _) = firstHeader.split()
    status = 200
    statusMessage = "OK"
    responseBody = ""
    key = path[1:]
    # method에 따라 알맞은 reponse message를 구성한다
    if (method == "GET"):
        # path에서 '/'를 제외한 값을 key로 사용 
        # path가 /일 경우 table의 모든 data를 전송한다
        if (path == "/"):
            responseBody = str(table)
        # 만약 key가 data table에 없을 경우 No Content 처리한다
        elif (key not in table):
            status, statusMessage = handleStatus204()
        else:
            responseBody = str({ key : table[key] })
    elif (method == "HEAD"):
        key = path[1:]
        # 만약 key가 data table에 없을 경우 No Content 처리한다
        if (key not in table):
            status, statusMessage = handleStatus204()
    elif (method == "POST"):
        table.update(eval(requestBody))
        responseBody = str({ key : table[key]})
        status, statusMessage = handleStatus201()
    elif (method == "PUT"):
        newDict = eval(requestBody)
        # 없던 key를 추가할 경우 state를 201 Created로 설정한다 아니라면 200 OK이다.
        if (key not in table):
            status, statusMessage = handleStatus201()
        table.update(newDict)
        responseBody = str({ key : table[key] })

    # Content-Length
    bodySize = len(responseBody)

    # response message를 구성한다
    responseMessage = f"HTTP/1.1 {status} {statusMessage}\r\nContent-Type: application/json\r\nContent-Length: {bodySize}\r\n\n"
    responseMessage += responseBody

    return responseMessage



# IPv4 주소를 지정하고, TCP를 사용한다
serverSocket = socket(AF_INET, SOCK_STREAM)
# server를 설정한 ip와 port binding 한다
serverSocket.bind((host, port))
# clinet의 요청을 대기한다
serverSocket.listen(1)
print("Server: listening...")

# client가 접속됐을 경우 새로운 socket과 client의 주소를 return값으로 받는다.
connectionSocket, clientAddress = serverSocket.accept()

# request-response를 주고 받는 while문
while True:

    # client로부터 request를 받는다
    data = connectionSocket.recv(1024)
    requestMessage = data.decode("utf-8")

    print("-----------REQUEST------------\n")
    print(requestMessage)
    print("------------------------------\n")

    # request 메시지를 해석하고 response를 보낸다
    try:
        connectionSocket.send(makeResponseMessage(requestMessage).encode("utf-8"))
    except:
        break


# server socket을 종료한다
serverSocket.close()
