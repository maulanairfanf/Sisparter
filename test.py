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

def download_file_handler():


    # handler ketika melakukan refresh folder server.
    def refresh_directory_handler():
        
        # judul untuk tiap message.
        title = "Server Directory"

        # matikan button untuk download file.
        
        # coba untuk get list directory dari server.
        try:    dir_list, exit_status = SERVER.get_dir_list()
        except: exit_status = -1

        # jika tidak ada error maka tampilkan seluruh file.
        if exit_status == 0:
            
            # aktifkan state dir list dan hapus isinya.
            txt_dir_list["state"] = "normal"
            txt_dir_list.delete("1.0", "end")
            
            # tulis setiap file di dir list.
            txt_dir_list.insert("end", "File List:\n")
            for file in dir_list: txt_dir_list.insert("end", f"- {file}\n")
            
            # matikan kembali state dir list dan aktifkan tombol download.
            txt_dir_list["state"] = "disabled"
            btn_downloads["state"] = "active"

        # directory dari server kosong.
        elif exit_status == 1: messagebox.showwarning(title, "There are no file stored on the server yet.")
        
        # error lain.
        else: messagebox.showwarning(title, f"Can't connect with server. Try checking the server first or contact server admin.")
    
    def download_handler():

        # judul untuk tiap message.
        title = "Download File"
        
        # get nama file yang mau di download.
        file_name = txt_file_name.get("1.0", "end").strip()

        # make sure client download file yang benar.
        if messagebox.askyesno(title, f"Are you sure you want to download '{file_name}'?"):

            # matikan state button download.
            btn_downloads["state"] = "disabled"
            
            # coba untuk download file.
            try:    file, exit_status = SERVER.download_file(file_name, USER_DATA)
            except: exit_status = -1

            # simpan file ke folder client.
            if exit_status == 0:
                
                # get path folder dan gabungkan dengan nama file.
                dir_path = filedialog.askdirectory()
                ful_path = os.path.join(dir_path, file_name)
                
                # simpan file.
                with open(ful_path, "wb") as f: f.write(file.data)
                
                # tampilkan pesan bahwa file sudah di download.
                messagebox.showinfo(title, f"'{file_name}' successfully downloaded.")
            
            # file tidak ditemukan di server.
            elif exit_status == 1: messagebox.showwarning(title, f"Can't download '{file_name}' because a file with that name is not exists. Please specify a different name.")
            
            # error yang lain.
            else: messagebox.showwarning(title, f"Can't connect with server. Try checking the server first or contact server admin.")
            
        # aktifkan kembali state button download.
        btn_downloads["state"] = "active"

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

