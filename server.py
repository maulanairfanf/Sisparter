import xmlrpc.client, socket, os
from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime

PORT     = 8080
HOSTNAME = socket.gethostname()
LOCAL_IP = "192.168.100.7"

# server selalu aktif.
def is_active(): return True

def upload_file(file, file_name, USER_DATA):

    # cek apakah file belum ada di data.
    if not file_name in os.listdir("data"):

        update_user_activity("upload", file_name, USER_DATA)

        # upload file ke server.
        with open(os.path.join("data", file_name), "wb") as f:
            f.write(file.data)
            
            return 0 # exit status 0 apabila upload berhasil.

    return 1 # exit status 1 apabila file sudah ada.

def download_file(file_name, USER_DATA):

    # cek apakah file ada di data.
    if file_name in os.listdir("data"):

        update_user_activity("download", file_name, USER_DATA)

        # ubah file ke bentuk biner dan return file-nya.
        with open(os.path.join("data", file_name), "rb") as f:
            file = f.read()
            file = xmlrpc.client.Binary(file)
            
            return file, 0 # exit status 0 apabila download berhasil.
    
    return None, 1 # exit status 1 apabila file tidak ada.

def get_dir_list():

    # get list dari data yang dimiliki server.
    dir_list = os.listdir("data")
    
    # jika isi folder-nya kosong maka exit status-nya 1.
    if len(dir_list) == 0:
        return None, 1
    
    return dir_list, 0 # jika ada isi folder-nya maka exit status-nya 0.

def update_user_activity(activity, file_name, USER_DATA):
    current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open("user_activity.file", "a") as f:
        f.write(f"{current_time} {USER_DATA['name']} {USER_DATA['ip']} {activity} {file_name}\n")

# buat folder data apabila tidak ada.
if not os.path.exists("data"): os.makedirs("data")

# aktifkan server-nya.
with SimpleXMLRPCServer((LOCAL_IP, PORT), allow_none=True) as server:
    print (f"Listening on port {PORT} with IP {LOCAL_IP}")

    # register seluruh function yang ingin dipakai.
    for func in [is_active, upload_file, download_file, get_dir_list]:
        server.register_function(func)

    server.serve_forever()