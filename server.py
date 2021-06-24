# import library
import xmlrpc.client, socket, os
from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime

# init hostname, local ip & port
HOSTNAME = socket.gethostname()
LOCAL_IP = "192.168.1.16"
PORT     = 8080

# function upload file
def handleUploadFile(file, fileName, USER):

    # check if file not exist on server
    if not fileName in os.listdir("storage"):

        # update user input with status, filename and user
        userInput("Upload-File", fileName, USER)

        # upload file to server.
        with open(os.path.join("storage", fileName), "wb") as f:
            f.write(file.data)
            
            # exit with status 200 if upload success.
            return 200

    # exit with status 400 if file exist.
    return 400

def handleGetFiles():

    # get files on the server
    files = os.listdir("storage")
    
    # if files is empty, exist with status 1 and return none
    if len(files) == 0:
        return None, 400
    
    # if files is exist, exit with status 0 and return files
    return files, 200

# function download file
def handleDownloadFile(fileName, USER):

    # check if file is exist on server.
    if fileName in os.listdir("storage"):

        # update user input with status, filename and user
        userInput("Download-File", fileName, USER)

        # change file to biner & return file to download
        with open(os.path.join("storage", fileName), "rb") as f:
            file = f.read()
            file = xmlrpc.client.Binary(file)
            
            # exit with status 0 if file exist & return file to download
            return file, 200
    
    # exit with status 1 if file is not exist and return none 
    return None, 400

# function update user input
def userInput(userInput, fileName, USER):
    # init current time with present
    currentTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # write user input on file 'user-history.txt'
    # with value Current Time, User Name, User IP, User Input & Filename
    with open("user-history.txt", "a") as f:
        f.write(f"{currentTime} {USER['name']} {USER['ip']} {userInput} {fileName}\n")

# create storage if server storage not exist
if not os.path.exists("storage"):
    os.makedirs("storage")

# turn on server.
with SimpleXMLRPCServer((LOCAL_IP, PORT), allow_none=True) as server:
    print (f"Listening on port {PORT} with IP {LOCAL_IP}")

    # register functions that will be used.
    for functions in [ handleUploadFile, handleDownloadFile, handleGetFiles ]:
        server.register_function(functions)

    server.serve_forever()