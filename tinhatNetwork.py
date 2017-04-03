from time import sleep
import socket

# set up socket, not currently threaded (used in main threads as of now)
#class socketSetup:

    #def __init__(self, host = '', port = 8000):
        #self.host = host
        #self.port = port
        #self.s = setupServer()
        #self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #print "Socket created."
        # TENTATIVE TESTING TO INITIALIZING socket, connection, and address through function calls
        #self.setupServer()
        #self.setupConnection()
        #self.conn = setupConnection()
    
def setupServer(host, port):
    # Create socket, notify user
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    print "Socket created"
    # Try binding socket
    try:
        s.bind((host, port))
    except socket.error as msg:
        print msg
    print "Socket bind complete"
    return s
        #return s

def setupConnection(sock):
    sock.listen(1)
    (conn, address) = sock.accept()
    print "Connected to : " + address[0] + ":" + str(address[1])
    return conn
        #return self.conn

    

#######################################
