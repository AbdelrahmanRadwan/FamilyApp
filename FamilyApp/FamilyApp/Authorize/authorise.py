import socket
import sys
from FamilyApp.Graph import auth_helper,config
import requests
import webbrowser
import server
import threading                     
#from Graph.config import client_id, client_secret

redir = 'http://localhost:4321'

def authCode():
    url = auth_helper.get_signin_url()
    print (url)
    webbrowser.open_new_tab(url)
    r = requests.get(url)
    try:
        r.raise_for_status()
        print(r.status_code )
    except requests.HTTPError:
        raise RuntimeError('unable to obtain authorization token')

    code = threading._start_new_thread(server.flaskThread())

    return code

def loginProcess():
    try:
        code = auth()
        token = auth_helper.get_token_from_code(code, redir)

        userInfoJson = auth_helper.get_user_info_from_token(token)

        #Register user now with the individual class
    except Exception as e:
        print(e)



#def authorizationCode():
#    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#    add = ('localhost', 4321)
#    print (sys.stderr, 'starting up on %s port %s' %add)
#    sock.bind(add)

#    sock.listen(1)

#    while True:
#        # Wait for a connection
#        print (sys.stderr, 'waiting for a connection')
#        connection, client_address = sock.accept()

#    try:
#            print (sys.stderr, 'connection from', client_address)

#            # Receive the data in small chunks and retransmit it
#            while True:
#                data = connection.recv(16)
#                print (sys.stderr, 'received "%s"' % data)
#                if data:
#                    print (sys.stderr, 'sending data back to the client')
#                    connection.sendall(data)
#                else:
#                    print (sys.stderr, 'no more data from', client_address)
#                    break
#    finally:
#            # Clean up the connection
#            connection.close()
