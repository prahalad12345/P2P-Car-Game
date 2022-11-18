
"""
main server script for running agar.io server

can handle multiple/infinite connections on the same
local network
"""
import socket
from _thread import *
import _pickle as pickle
import time
import random
import math
import pickle

# setup sockets
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Set constants
PORT = 4000

connections=0
W, H = 800, 600

HOST_NAME = socket.gethostname()
SERVER_IP = "10.196.6.19"

# try to connect to server
try:
    S.bind((SERVER_IP, PORT))
except socket.error as e:
    print(str(e))
    print("[SERVER] Server could not start")
    quit()

S.listen()  # listen for connections

print(f"[SERVER] Server Started with local ip {SERVER_IP}")

# dynamic variables
players = {}
enemycar=(random.randrange(310, 450),-600)
crashed = {}
iddd=0
_id=0
start = False
speed=5
stat_time = 0
game_time = "Starting Soon"
nxt = 1    


def enemy_car_generate():
    global enemycar,H,speed
    if enemycar[1]>H:
        enemycar=(random.randrange(310, 450),-100)
    else:
        enemycar=(enemycar[0],enemycar[1]+speed)


def threaded_client(conn, idd):

	global connections, players ,enemycar ,iddd ,speed
	print(1)
	current_id = idd
	print(iddd)
	# recieve a name from the client
	#data = conn.recv(16)
	

	# Setup properties for each new player
	players[current_id] = (360,480)

	# pickle data and send initial info to clients
	print()
	conn.send(str.encode(str(current_id)))
	enemy_car_generate()
	print(enemycar)
	while True:
		print(enemycar)

		try:
			# Recieve data from client
			data = conn.recv(1024)


			print(data[1])

			if not players[current_id]:
				enemy_car_generate()
				send_data=pickle.dumps(enemycar)
				conn.send(send_data)
			else:
				# any other command just send back list of players
				enemy_car_generate()
				send_data=pickle.dumps(enemycar)
				conn.send(send_data)

			# send data back to clients
			iddd+=1
			if iddd%1000==0:
				speed+=1

		except Exception as e:
			print(e)
			break  # if an exception has been reached disconnect client

		time.sleep(0.001)

	# When user disconnects	
	print("[DISCONNECT] Name: , current_id, disconnected")

	connections -= 1 
	del players[current_id]  # remove client information from players list
	conn.close()  # close connection


# MAINLOOP



print("[GAME] Setting up level")
print("[SERVER] Waiting for connections")

# Keep looping to accept new connections
while True:
	
	host, addr = S.accept()
	print("[CONNECTION] Connected to:", addr)

	# start game when a client on the server computer connects
	if addr[0] == SERVER_IP and not(start):
		start = True
		start_time = time.time()
		print("[STARTED] Game Started")

	# increment connections start new thread then increment ids
	connections += 1

	start_new_thread(threaded_client,(host,_id))

	_id += 1

# when program ends
print("[SERVER] Server offline")