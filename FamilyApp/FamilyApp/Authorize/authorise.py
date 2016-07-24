import socket
import time
import sys
import auth_helper,config
import requests
import webbrowser
import server
import threading                     
#from Graph.config import client_id, client_secret

redir = 'http://localhost:4321'



def authCode():

    try:
        t= threading.Thread(target = server.flaskThread)
        t.start()
    except:
        print("Server failed to start")

    url = auth_helper.get_signin_url(redir)
    webbrowser.open_new(url)

    try:
        print("postthread")
        r = requests.get(url)
   
        r.raise_for_status()
        print('\n\nStatus code ' + str(r.status_code ))
    except:
        print('unable to obtain authorization token')
    code = receiveAuth()
    print ("\ncode:" +code)
    return code

def dummy():
    time.sleep(5)
    print("hello")


def loginProcess():
    try:
        code = authCode()
        token = auth_helper.get_token_from_code(code, redir)
        print("token" , token)
        userInfoJson = auth_helper.get_user_info_from_token(token)
        return userInfoJson
        #Register user now with the individual class
    except Exception as e:
        print(e)


def receiveAuth():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    add = ('localhost', 4321)
    print (sys.stderr, 'starting up on %s port %s' %add)
    sock.bind(add)

    sock.listen(1)

    while True:
        # Wait for a connection
        print (sys.stderr, 'waiting for a connection')
        connection, client_address = sock.accept()

    try:
            print (sys.stderr, 'connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = data + connection.recv(16)
                print (sys.stderr, 'received "%s"' % data)
                if data:
                    return data
                    print (sys.stderr, 'sending data back to the client')
                    connection.sendall(data)
                else:
                    print (sys.stderr, 'no more data from', client_address)
                    break
    finally:
            # Clean up the connection
            connection.close()