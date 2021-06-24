import xmlrpc.client, tkinter, socket, os
from tkinter import filedialog, messagebox

# Init server_IP
SERVER_IP = "192.168.100.7"
PORT      = "8080"

# Init server proxy.
SERVER    = xmlrpc.client.ServerProxy(f"http://{SERVER_IP}:{PORT}")

# Init hostname and local_ip
HOSTNAME  = socket.gethostname()
LOCAL_IP  = socket.gethostbyname(HOSTNAME)

USER_DATA = {"name" : HOSTNAME, "ip" : LOCAL_IP}

def upload_file_handler():

    # judul untuk tiap message.
    title = "File Upload"

    # get path dan nama dari file yang akan diupload.
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)

    # matikan state button download dan upload.
    # change_file_updn_btn_state("disabled")
    
    # untuk memastikan bahwa client meng-upload file yang benar.
    if file_path and messagebox.askyesno(title, f"Are you sure you want to upload '{file_name}' to server?"):
        
        # buka file-nya terlebih dahulu.
        with open(file_path, "rb") as f:

            file = f.read()
            
            # coba untuk upload file.
            try:    exit_status = SERVER.upload_file(xmlrpc.client.Binary(file), file_name, USER_DATA)
            except: exit_status = -1
            
            # menandakan upload sukses tanpa ada kendala.
            if exit_status == 0: print("successfully uploaded.")
                
            
            # upload tidak berhasil karena file sudah ada di server.
            elif exit_status == 1: print("Upload gagal")
            
            # error yang tidak diketahui.
            else: print("Can't connect with server. Try checking the server first or contact server admin.")

    # aktifkan kembali state button download dan upload.
    # change_file_updn_btn_state("active")

def uploadDownload():
    print("1.Upload File \n2.Download File")
    print("pilih : ")

    chooseBool = False

    while (chooseBool == False):
        choose = int(input())
        if(choose == 1 or choose == 2):
            if(choose == 1):
                upload_file_handler()
            if(choose == 2):
                print('belum ada')
            chooseBool = True
        else:
            print("pilihan salah silahkan pilih kembali : ")

def check_server_handler():

    # matikan button upload dan download.
    
    print(SERVER)
    
    # cek apakah server aktif.
    try:    is_server_on = SERVER.is_active()
    except: is_server_on = False
    
    # jika server aktif maka tampilkan dan aktifkan kembali button upload dan download.
    if is_server_on:
        print('server active')
        uploadDownload()
    # jika server mati maka tampilkan info bahwa server mati.
    else: 
        print('server inactive')
        # lbl_server_status.config(text="Server is not active.", fg="red")

check_server_handler()

