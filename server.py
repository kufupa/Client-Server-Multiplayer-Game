# libraries to handle connections to server
import sys
from  _thread import *
import socket

#
server = "192.168.2.201" # ENTER SERVERS IPV4 ADDRESS
#

port = 5555 # commonly open port


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPV4 address, sock_stream represents how server string previously defined comes in


# bind server and port to socket
try: # have to try and except bc port might already be in use so it might not work
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2) # open port and listen for clients - no parameters means infinite number of clients, otherwise enter max number of clients
# ^ i want 2 connections as 2 players
print("\nServer started, waiting for connections")

positions = [ (775, 300, 0, 5), (100, 300, 0, 5) ] # (775, 300) for red, (100, 300) for yellow
# positions[0] = red, 1 == yellow

def threaded_client(conn, server_player):
    conn.send(str.encode(str(server_player))) # send validation message to client that we're connected
    
    reply = ""
    while True: # want to continuosly run while client is connected

        try:
            data = read_pos(conn.recv(2048).decode()) # how many bits we're gonna recieve from connection ; more bits = longer to take connection so try keep as small as possible
            positions[server_player] = data

            if not data: # if we try get data from client but nothing is there, means we can disconnect
                print("Disconnected")
                break
            else:
                if server_player == 1:
                    reply = positions[0] # send other player's positions
                else:
                    reply = positions[1]

            conn.sendall(str.encode(make_pos(reply))) # encode data so we can send it over internet securely
        
        except:
            break
    
    print("Lost connection")
    conn.close()


# game code
def read_pos(str):
    spl = str.split(", ")
    return int(spl[0]), int(spl[1]), int(spl[2]), int(spl[3])

def make_pos(tuple):
    return str(tuple[0]) + ", " + str(tuple[1]) + ", " + str(tuple[2]) + ", " + str(tuple[3])

server_player = 0
while True: # continuosly look for connections - and carry out relevant procedures
    conn, addr = s.accept()
    print("Connected to: ", addr)

    # use a thread which is a process running in background
    # means that we dont have to wait for functions to finish executing
    # ^ so we can keep looking for new connections - otherwise would lose / miss data
    start_new_thread(threaded_client, (conn, server_player)) # start_new_thread = function from _thread
    server_player += 1

# tims code
