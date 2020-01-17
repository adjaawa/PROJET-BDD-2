import socket, argparse
import sys
import traceback
from threading import Thread
import getpass
import connect

def server () :

    host = '127.0.0.1'
    port = 8888

    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt (socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ('Socket created')
    try :
        sock.bind ( (host, port) )
    except :
        print ('Bind failed. Error :' + str (sys.exc_info()))
        sys.exit()

    sock.listen (5)
    print ('Listening at : ' , sock.getsockname())

    while True :
        connection , address = sock.accept ()
        print ('We have accepted a connection from ', address)
        ip, port = str (address[0]), str (address[1])
        print ('Connected with ' + ip + ' : ' + port)
        try :
            Thread (target = client_thread, args = (connection , ip,port)).start()
        except:
            print ('Thread did not start.')
            traceback.print_exc()
            sock.close()

def authenticate () :

    print ('\n------- A U T H E N T I C A T I O N ------\n')
    username = input ('Username > ')
    password = getpass.getpass ('Password > ')
    print ('------- ------------ --------- ---- ------\n')
    return 'Authentication ' + ' ' + username + ' ' + password

def client () :

    host = '127.0.0.1'
    port = 8888

    sock = socket.socket (socket.AF_INET, socket.SOCK_STREAM)

    try :
        sock.connect ( (host, port) )
    except :
        print ('Connection error')
        sys.exit ()

    # Authentification

    sock.sendall (authenticate ().encode('utf8'))
    authentication = sock.recv (5120).decode('utf8')

    while authentication == 'False' :
        print ('Authentication failed. Try again.')
        sock.sendall (authenticate ().encode('utf8'))
        authentication = sock.recv (5120).decode('utf8')

    print ('Connected !')
    print ("Enter 'quit' to exit\n")
    message = input ('>> ')

    while message != 'quit' :
        sock.sendall (message.encode ('utf8'))
        #if sock.recv (5120).decode('utf8') == '-':
        #    pass
        print (sock.recv(5120).decode('utf8'))
        message = input ('>> ')
    sock.send (b'--quit--')
    
def client_thread (connection, ip, port, max_buffer_size = 5120):
    
    is_active = True

    while is_active:

        client_input = receive_input (connection, max_buffer_size)

        if '--QUIT-- ' in client_input :

            print ('Client is requesting to quit')
            connection.close()
            print ('Connection ' + ip + ':' + port + ' closed')
            is_active = False

        else :
            print ('Processed result : {}'.format(client_input))
            connection.sendall (client_input.encode('utf8'))

def receive_input (connection, max_buffer_size):

    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof (client_input)

    if client_input_size > max_buffer_size:
        print ('Max input size')
    
    decoded_input = client_input.decode ('utf8').rstrip()

    result = process_input (decoded_input)

    return result


def process_input (input_str):
  
    if (input_str.startswith('Authentication')):
        return connect.connect (input_str)

    if (input_str.startswith (('Create database').casefold())) :
        return ('Create database statement')

    elif (input_str.startswith (('Create table').casefold())):
        return ('Create table statement')

    elif (input_str.startswith (('Insert into').casefold())):
        return ('Insert into statement')

    elif (input_str.startswith (('Select').casefold())) :
        return ('Select statement')

    elif (input_str.startswith (('Create user').casefold())) :
        return connect.create_user(input_str)

    elif (input_str.startswith (('show databases').casefold())) :
        return ('Show databases')

    else :
        return ('Not a sql command')

if __name__ == '__main__' : 
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='SQL') 
    parser.add_argument('role', choices=choices, help ='Role to play') 
    args = parser.parse_args()
    function = choices [args.role]
    function ()
