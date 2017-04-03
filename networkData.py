import tinhatNetwork as tn
import socket
import Queue
import threading

# Thread class to receive data
class dataReadPi(threading.Thread):

    def __init__(self, ready, waiting, commandQueue, host = '', port = 8000):
        super(dataReadPi, self).__init__()
        self.host = host
        self.port = port
        self.ready = ready
        self.waiting = waiting
        self.stopRequest = threading.Event()
        self.commandQueue = commandQueue

    def run(self):
        
        sock = tn.setupServer(self.host, self.port)
        conn = tn.setupConnection(sock)
        while not self.stopRequest.isSet():
            data = conn.recv(1024)
            # set ready internally
            self.ready.set()
            if self.ready.isSet() and not self.waiting.isSet():
                self.commandQueue.put(data)
                #clear ready internally
                self.ready.clear()
            elif self.waiting.isSet():
                #self.waiting.wait()
            continue
        conn.close()

    def join(self, timeout = None):
        self.stopRequest.set()
        super(dataReadPi, self).join(timeout)

# Thread class to send data from pi
class dataSendPi(threading.Thread):

    def __init__(self, ready, waiting, sensorQueue, host = "localhost", port = 8001):
        super(dataSendPi, self).__init__()
        self.host = host
        self.port = port
        self.ready = ready
        self.waiting = waiting
        self.stopRequest = threading.Event()
        self.sensorQueue = sensorQueue
        
    def run(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        #conn = setupConnection(socket)
        #socket = socketSetup(self.host, self.port)
        self.ready.clear()
        #self.waiting.set()
        while not self.stopRequest.isSet():
            if self.ready.isSet() and not self.waiting.isSet():
                #self.waiting.wait()
                if not sensorQueue.empty():
                    sensorSend = self.sensorQueue.get()
                    sock.send(sensorSend)
                    self.ready.clear()
            elif self.waiting.isSet():
                #self.waiting.wait()
                #self.waiting.set()
            continue
        sock.close()

    def join(self, timeout = None):
        self.stopRequest.set()
        super(dataSendPi, self).join(timeout)

class dataReadConsole(threading.Thread):
    def __init__ (self, ready, waiting, sensorQueue, host = '', port = 8001):
        super(dataReadConsole, self).__init__()
        self.host = host
        self.port = port
        self.ready = ready
        self.waiting = waiting
        self.stopRequest = threading.Event()
        self.sensorQueue = sensorQueue

    def run(self):
        sock = tn.setupServer(self.host, self.port)
        conn = tn.setupConnection(sock)
        while not self.stopRequest.isSet():
            data = conn.recv(1024)
            self.ready.set()
            if self.ready.isSet()and not self.waiting.isSet():
                self.sensorQueue.put(data)
                self.ready.clear()
            elif self.waiting.isSet():
                #self.waiting.wait()
            continue
        conn.close()

    def join(self, timeout = None):
        self.stopRequest.set()
        super(dataReadConsole, self).join(timeout)

class dataSendConsole(threading.Thread):

    def __init__(self, ready, waiting, commandQueue, host = '', port = 8000):
        super(dataSendConsole, self).__init__()
        self.host = host
        self.port = port
        self.ready = ready
        self.waiting = waiting
        self.stopRequest = threading.Event()
        self.commandQueue = commandQueue
        
    def run(self):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        self.ready.clear()
        #self.waiting.set()
        while not self.stopRequest.isSet():
            if self.ready.isSet() and not self.waiting.isSet():
                if not self.commandQueue.empty():
                    commandSend = self.commandQueue.get()
                    sock.send(commandSend)
                    self.ready.clear()
            elif self.waiting.isSet():
                #self.waiting.wait()
            continue
        sock.close()
                    

    def join(self, timeout = None):
        self.stopRequest.set()
        super(dataSendConsole, self).join(timeout)
