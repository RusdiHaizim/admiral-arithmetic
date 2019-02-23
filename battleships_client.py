#my_address = 192.168.137.63
#client1.py
import socket
import random
import time
from definitions import *

'''
1) Initialize arrays
2) Use GUI to set up ships on enemy_map
3) Send my_map to other pi as a 24-bit package
4) Standby for start (mine_sent && other_received)

#857lj99*

Ships:

3 x size 1
2 x size 2
1 x size 3

overall: 3+4+3 = 10/24 tiles have a ship.

Structure of Question List: consists of Question objects

'''

#array 1 (default) - map of hit/miss/not hit on enemy's side
#array 2 - map of my ships

global is_player_1
is_player_1 = 0

#global addr
#global c
#global server
#ships

ship_list = []
ship_list.append(Ship("Corvette 1",1))
ship_list.append(Ship("Corvette 2",1))
ship_list.append(Ship("Corvette 3",1))
ship_list.append(Ship("Frigate 1",2))
ship_list.append(Ship("Frigate 2",2))
ship_list.append(Ship("Aircraft Carrier",3))


#questions

qn_lst = []

for i in range(24):
    qn_lst.append(Question("+"))


def setup_myships():
    '''
    connect to server
    '''
    '''
    get question list from server (?)

    for each ship:
        add in if tiles are valid (X0,X1,Y0,Y1)
        {value for value in variable

    submit confirmation (check whether sent or receives)


    '''
    sent, received = False, False

    coords = [(2,1),(3,2),(4,1),(0,0),(0,2),(4,0)]
    for i in range(6):
        x = coords[i][0]
        y = coords[i][1]
        my_map.put_ship(ship_list[i],x,y)


##    for ship in ship_list:
##        print("Where would you like to place your "+ship.name+", Admiral?")
##        x = int(input("Enter x coordinate: "))
##        y = int(input("Enter y coordinate: "))
##        if is_valid(ship,my_map,x,y):
##            my_map.put_ship(ship,x,y)
##            #update_display
##            print("Roger.")
##        else:
##            while not is_valid(ship,my_map,x,y):
##                print("Sir, please provide a valid coordinate.")
##                x = int(input("Enter x coordinate: "))
##                y = int(input("Enter y coordinate: "))
##            my_map.put_ship(ship,x,y)
##            #update_display
##            print("Roger.")


    my_map.message = my_map.prepare_string()

    IP = '172.20.10.10'
    PORT = 8080
    global server
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    if is_player_1:
        server.bind((IP, PORT))
        server.listen(5)
        c,addr = server.accept() #client, address
        print("Got connection from", addr)
    else:
        while (1):
            try:
                print("attempt")
                server.connect((IP,PORT))
                print("connected")
                break
            except Exception as e:
                print(e)



    while (not received) and (not sent):
        try:
            if is_player_1:
                if not sent:
                    c.send(bytes(my_map.message,'UTF-8'))
                    sent = True

                if not received:
                    data = c.recv(1024)
                    received = True
                    enemy_map.read_from_string(data)

            else:
                if not received:
                    data = server.recv(1024)
                    print("received")
                    received = True
                    enemy_map.read_from_string(data)

                if not sent:
                    print("sent")
                    server.send(bytes(my_map.message,'UTF-8'))
                    sent = True

        except Exception as e:
            print(e)


# Loop:

def loop():
    qn = 0
    while True:
        '''
        display qn no
        display qn
        wait for user input
        if wrong, do nothing
        else, wait for user input for attack vector
        start 5 second timer
        while (timer<=5 or invalid/no input), wait for input
        send attack vector if valid
        else send random attack vector
        '''

        # fetch and ask question
        print("Question #"+str(qn+1)+"\n")
        cur = qn_lst[qn]
        print(cur)
        ans = int(input("Enter your answer here: "))
        while (not cur.check_correct(ans)):
            ans = int(input("Enter your answer here: "))

        #choosing of attack vector
        start = time.time()
        x = int(input("Enter x coordinate to attack: "))
        y = int(input("Enter y coordinate to attack: "))
        while (x<0 or x>7 or y<0 or y>3):
            x = int(input("Enter x coordinate to attack: "))
            y = int(input("Enter y coordinate to attack: "))
        end = time.time()
        if (end - start)>10:
            print("Too slow, Admiral! We missed the window to attack!")
            x = randint(0,7)
            y = randint(0,2)
        qn += 1
        if qn == 24:
            break

        #sending of attack vector
        if(is_player_1):
            c.send(bytes(("%s,%s"%(x,y)),'UTF-8'))
        else:
            server.send(bytes(("%s,%s"%(x,y)),'UTF-8'))

setup_myships()

if is_player_1:
    newthread = ServerThread(addr,c)
else:
    newthread = ClientThread(server)

newthread.start()

loop()

if not is_player_1:
    server.send(bytes("bye",'UTF-8'))
newthread.join()

