import socket
import time
import sys
import auth_helper,config
import requests
import webbrowser
import server
import threading   
import json   
from AuthInfo import GraphInfo              
#from Graph.config import client_id, client_secret

redir = 'http://localhost:4321'



def authCode():


    try:
        t= threading.Thread(target = server.flaskThread)
        t.start()
    except:
        print("Server failed to start")

    url = auth_helper.get_signin_url(redir)
    webbrowser.open_new_tab(url)

    try:
       # print("postthread")
        r = requests.get(url)
   
        r.raise_for_status()
        #print('\n\nStatus code ' + str(r.status_code ))
    except:
        print('unable to obtain authorization token')
    #print("count" +str(threading.active_count()))
    while(threading.activeCount() >1):
        time.sleep(2)
    codeFile = open("Textfiles\\authCode.txt",'r')
    authenticationCode = codeFile.readline()
    codeFile.close()

    return authenticationCode

def dummy():
    time.sleep(5)
    print("hello")


def getIDandUserPrincipleId(access_token):
    url = "https://graph.microsoft.com/v1.0/me"

    headers = { 
    'Authorization' : 'Bearer {0}'.format(access_token),
    'Accept' : 'application/json'
    }

    r = requests.get(url = url , headers = headers)
    print(r)
    if (r.status_code == requests.codes.ok):
        r = r.json()
        print(r)
        idd = r['id']
        name = r['userPrincipalName']
        return r['id'], r['userPrincipalName']
        #r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)
   

def loginProcess():
    userGraphInfo = GraphInfo()
    try:
        userGraphInfo.auth_code = authCode()
        access_token_json = auth_helper.get_token_from_code(userGraphInfo.auth_code, redir)
        
        userGraphInfo.access_token = access_token_json["access_token"]
        userGraphInfo.refresh_token = access_token_json["refresh_token"]
        userGraphInfo.expires_in = access_token_json["expires_in"]
        userGraphInfo.id_token = access_token_json["id_token"]

        userGraphInfo.id , userGraphInfo.userPrincipleName = getIDandUserPrincipleId(userGraphInfo.access_token)

        userGraphInfo.user_info_json = auth_helper.get_user_info_from_token(userGraphInfo.id_token)
        #print( "User Info" + json.dumps(userGraphInfo.user_info_json))
        return userGraphInfo
        #Register user now with the individual class
    except Exception as e:
        print(e)


def receiveAuth():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    add = (socket.gethostname(), 4321)
    #print (sys.stderr, 'starting up on %s port %s' %add)
    sock.bind(add)

    sock.listen(1)

    while True:
        # Wait for a connection
        #print (sys.stderr, 'waiting for a connection')
        connection, client_address = sock.accept()
        #print("\naddress" + client_address)
    try:
            #print (sys.stderr, 'connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = data + connection.recv(16)
                #print (sys.stderr, 'received "%s"' % data)
                if data:
                    return data
                else:
                    #print (sys.stderr, 'no more data from', client_address)
                    break
    finally:
            # Clean up the connection
            connection.close()