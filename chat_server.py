import socket
import threading,binascii

HOST=input('enter Host (default : 127.0.0.1) ')
if HOST=='' or HOST.isspace==True:
    HOST="127.0.0.1"
    
PORT=input('(default-10001) PORT : ')
if PORT=='' or PORT.isspace==True:
    PORT=8080
else:
    PORT=int(PORT)
MAX_CLIENTS=input('how many can join (ex:10): ')
if MAX_CLIENTS=='' or MAX_CLIENTS.isspace==True:
    MAX_CLIENTS=10
else:
    MAX_CLIENTS=int(MAX_CLIENTS)
BUFFER_SIZE = 1024





class ChatServer:
    '''
    class for chat server
    '''
    def __init__(self, host, port):
        print("init server...")
        self.all_users = []
        #create socket and listen new connections
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((HOST, PORT))
        self.sock.listen(MAX_CLIENTS)
        print("server: OK")
        print("started")
        
        
    def run(self):
        '''
        function for receiving new connection,
        for creating new thread, which handle own clients.
        '''
        while True:
            conn, addr = self.sock.accept()
            tr = threading.Thread(
                                target=self.client_handler, 
                                args=(conn,)
                                )
            tr.daemon = True
            tr.start()
            
    def client_handler(self, conn):
        '''
        function for handling new connection
        '''
        
        #first message is client name
        name = conn.recv(BUFFER_SIZE)
        name =binascii.a2b_uu(name).decode()
        print(name,'joined')
        hello_string = "Hello, {}. Users online is {}".format(
                                                    name, 
                                                    len(self.all_users)
                                                    )
        conn.sendall(binascii.b2a_uu(hello_string.encode()))
        self.all_users.append((conn, name))
        msg_to_all = " Entered chat!".format(name)
        self.send_message_to_others((conn, name), msg_to_all)    
        
        #infinite loop for receiving messages from client
        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            data =binascii.a2b_uu(data).decode()
            #print(name + ' ' + data)
            self.send_message_to_others((conn, name), data)    
        #client left chat
        conn.sendall(b'By')
        self.send_message_to_others(
                                (conn, name), 
                                " ~ left the chat! ~".format(name)
                                )    
        self.delete_user(conn)
        
    def delete_user(self, del_user):
        '''
        function for delete client from list all_users
        '''
        for i in range(len(self.all_users)):
            if self.all_users[i][0] == del_user:
                del self.all_users[i]
                break

    def send_message_to_others(self, from_user, message):
        '''
        function for sending message to all client except sender
        '''
        if len(self.all_users) > 1:
            for user in self.all_users:
                if user[0] != from_user[0]:
                    msg = "{}: {}".format(from_user[1], message)
                    user[0].sendall(binascii.b2a_uu(msg.encode()))
                    #print("message send")
                    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, tb):
        print("server is going down.")

with ChatServer(HOST, PORT) as chat:
    chat.run()
