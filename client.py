# Import library
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

# ubah state dari button download dan upload.
# bisa "active" atau "disabled".
def change_file_updn_btn_state(state):
    btn_file_upload["state"] = state
    btn_file_dnload["state"] = state

def check_server_handler():

    # matikan button upload dan download.
    change_file_updn_btn_state("disabled")
    
    print(SERVER)
    
    # cek apakah server aktif.
    try:    is_server_on = SERVER.is_active()
    except: is_server_on = False
    
    # jika server aktif maka tampilkan dan aktifkan kembali button upload dan download.
    if is_server_on:
        print('server active')
        lbl_server_status.config(text="Server is active.", fg="green")
        change_file_updn_btn_state("active")
    
    # jika server mati maka tampilkan info bahwa server mati.
    else: 
        print('server inactive')
        lbl_server_status.config(text="Server is not active.", fg="red")


def upload_file_handler():

    # judul untuk tiap message.
    title = "File Upload"

    # get path dan nama dari file yang akan diupload.
    file_path = filedialog.askopenfilename()
    file_name = os.path.basename(file_path)

    # matikan state button download dan upload.
    change_file_updn_btn_state("disabled")
    
    # untuk memastikan bahwa client meng-upload file yang benar.
    if file_path and messagebox.askyesno(title, f"Are you sure you want to upload '{file_name}' to server?"):
        
        # buka file-nya terlebih dahulu.
        with open(file_path, "rb") as f:

            file = f.read()
            
            # coba untuk upload file.
            try:    exit_status = SERVER.upload_file(xmlrpc.client.Binary(file), file_name, USER_DATA)
            except: exit_status = -1
            
            # menandakan upload sukses tanpa ada kendala.
            if exit_status == 0: messagebox.showinfo(title, f"'{file_name}' successfully uploaded.")
            
            # upload tidak berhasil karena file sudah ada di server.
            elif exit_status == 1: messagebox.showwarning(title, f"Can't upload '{file_name}' because a file with that name already exists. Please specify a different name.")
            
            # error yang tidak diketahui.
            else: messagebox.showwarning(title, f"Can't connect with server. Try checking the server first or contact server admin.")

    # aktifkan kembali state button download dan upload.
    change_file_updn_btn_state("active")

def download_file_handler():

    # handler ketika window download ditutup.
    def download_window_closing():
        download_window.grab_release()
        download_window.destroy()

    # handler ketika melakukan refresh folder server.
    def refresh_directory_handler():
        
        # judul untuk tiap message.
        title = "Server Directory"

        # matikan button untuk download file.
        btn_downloads["state"] = "disabled"
        
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

    #========================= DOWNLOAD FILE WINDOW ==============================
    download_window = tkinter.Toplevel(main_window)

    download_window.title("Download File")
    download_window.minsize(750, 500)

    download_window.grab_set()

    for i in range(2):
        download_window.rowconfigure(0, weight=1)
        download_window.columnconfigure(i, weight=1)

    #---------------------------- FRAME CONTROLS ---------------------------------
    frame_controls = tkinter.Frame(download_window, relief=tkinter.RAISED)
    frame_controls.grid(row=0, column=0)

    # File Name
    frame_file_name = tkinter.Frame(frame_controls, relief=tkinter.RAISED)
    frame_file_name.grid(row=0, padx=10, pady=10)

    lbl_file_name = tkinter.Label(master=frame_file_name, text="File Name :")
    txt_file_name = tkinter.Text(master=frame_file_name, height=1, width=20)

    lbl_file_name.grid(row=0, column=0)
    txt_file_name.grid(row=0, column=1)

    # Control Buttons
    frame_control_btn = tkinter.Frame(frame_controls, relief=tkinter.RAISED)
    frame_control_btn.grid(row=1)

    btn_downloads = tkinter.Button(frame_control_btn, text="Download File", command=download_handler)
    btn_flrefresh = tkinter.Button(frame_control_btn, text="Refresh File List", command=refresh_directory_handler)

    btn_downloads.grid(row=0, column=0, padx=5)
    btn_flrefresh.grid(row=0, column=1, padx=5)
    #---------------------------- FRAME CONTROLS ---------------------------------

    #------------------------------- DIR LIST ------------------------------------
    txt_dir_list = tkinter.Text(master=download_window, width=60)
    txt_dir_list.grid(row=0, column=1, sticky="nswe")
    
    txt_dir_list["state"] = "disabled"
    #------------------------------- DIR LIST ------------------------------------

    refresh_directory_handler()

    download_window.protocol("WM_DELETE_WINDOW", download_window_closing)
    #========================= DOWNLOAD FILE WINDOW ==============================

#============================= MAIN WINDOW ===================================
main_window = tkinter.Tk()

main_window.title("App Gabut")
main_window.minsize(190, 125)

for i in range(3):
    main_window.rowconfigure(i, minsize=10, weight=1)
    main_window.columnconfigure(0, minsize=10, weight=1)

# Server Status
lbl_server_status = tkinter.Label(master=main_window, text='')
lbl_server_status.grid(row=0, pady=10)

#======================== FRAME UPLOAD DOWNLOAD =============================
frame_updown = tkinter.Frame(master=main_window, relief=tkinter.RAISED)
frame_updown.grid(row=1, padx=5)

# Download Upload Buttons
btn_file_upload = tkinter.Button(master=frame_updown, text="Upload File", command=upload_file_handler)
btn_file_dnload = tkinter.Button(master=frame_updown, text="Download File", command=download_file_handler)

btn_file_upload.grid(row=0, column=0, padx=5)
btn_file_dnload.grid(row=0, column=1, padx=5)
#======================== FRAME UPLOAD DOWNLOAD =============================

# Check Server
btn_check_server = tkinter.Button(master=main_window, text="Check Server", command=check_server_handler)
btn_check_server.grid(row=2, pady=10)

check_server_handler()
#============================= MAIN WINDOW ===================================

main_window.mainloop()