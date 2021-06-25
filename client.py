# import library
import xmlrpc.client, tkinter, socket, os
from tkinter import filedialog, messagebox

# init server ip and port
SERVER_IP = "192.168.1.16"
PORT      = "8080"

# init server proxy.
SERVER    = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:{PORT}")

# init hostname and local ip
HOSTNAME  = socket.gethostname()
LOCAL_IP  = socket.gethostbyname(HOSTNAME)

# init user
USER = {
    "name": HOSTNAME,
    "ip": LOCAL_IP
}

# function to get user input
def handleUserInput():

    # get user input
    # if user type '1' => Upload File
    # if user type '2' => Download File
    userInput = int(input(
        "--- Type the number of actions below --- \n"
        "1. Upload File \n"
        "2. Download File \n"
        "Choose your action: "
    ))

    # return user input
    return userInput

# function upload file
def handleUploadFile():

    # get file path
    filePath = filedialog.askopenfilename()

    # get file name
    fileName = os.path.basename(filePath)

    # show upload file dialog confirmation 
    if filePath and messagebox.askyesno("Upload File", f"Are you sure to upload '{fileName}' to server?"):
        
        # open file
        with open(filePath, "rb") as f:

            # read file
            file = f.read()

            # separator
            print('\n')
            
            # try to upload file
            try:

                # get response upload file from server 
                response = SERVER.handleUploadFile(xmlrpc.client.Binary(file), fileName, USER)

                # if response == 200, then print success to upload file
                if response == 200:
                    print("Success to upload file")
                
                # if response == 400, then print failed to upload file
                elif response == 400:
                    print('Failed to upload file, file already exist')
            
            # handle exeption upload file
            except:
                print('Server Error')
            
            # separator
            print('\n')

# function download file
def handleDownloadFile():

    # separator
    print('\n')
    
    # try to get files on server
    try:

        # get response & files from server
        files, response = SERVER.handleGetFiles()

        # if response == 200
        if (response == 200):

            print('--- Type the number of file below ---')

            # loop files and print files
            for i in range(len(files)):
                print(f"{i + 1}. {files[i]}")
            
            # get user input to choose file
            inputUser = int(input('Choose file to download: '))

            # get fileName
            fileName = files[inputUser - 1]

            # try to download file.
            try:

                # get file and response from server
                file, response = SERVER.handleDownloadFile(fileName, USER)

                # separator
                print('\n')
                
                # if response == 200
                if (response == 200):

                    # get directory folder
                    dirName = filedialog.askdirectory()

                    # merge directory name and file name
                    path = os.path.join(dirName, fileName)
                    
                    # open path
                    with open(path, "wb") as f:

                        # save file
                        f.write(file.data)
                    
                    # print success to download file
                    print('Success to download file')
                
                # print failed to download file
                else:
                    print('Failed to download file, file is not found')
            
            # exeption dowload file
            except:
                print('Server Error')

        # print storage empty
        else:
            print('server storage empty')

    # exeption get files
    except:
        print('Server Error')
    
    # separator
    print('\n')

# function main program
def main():

    # withdraw tkinter main window
    tkinter.Tk().withdraw()
    
    # init user input
    userInput = handleUserInput()

    # if user input == 1, do upload file
    if (userInput == 1):
        handleUploadFile()

    # else user input == 2, do download file
    else:
        handleDownloadFile()

# run main program with infinite loop
while True:
    main()