import threading
from random import *


class ServerThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
    def run(self):
        msg = ''
        while True:
            data = self.csocket.recv(16)
            print(data)
            msg = data.decode()
            if msg=='bye':
                break
            x = int(msg[0])
            y = int(msg[2])
            my_map.update_on_attack(x,y)
            if my_map.message == 1:
                print("You've been hit at ("+x+','+y+"), sir!\n")
            #update display

        print ("Client at ", clientAddress , " disconnected...")

class ClientThread(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.csocket = client
    def run(self):
        msg = ''
        while True:
            data = self.csocket.recv(16)
            msg = data.decode()
            if exitflag:
                break
            x = int(msg[0])
            y = int(msg[2])
            my_map.update_on_attack(x,y)
            if my_map.message == 1:
                print("You've been hit at ("+x+','+y+"), sir!\n")
            #update display
        self.csocket.close()

class Ship(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_name(self):
        return self.name

class Question(object):
    def __init__(self,operation):
        self.op = " "+operation+" "
        x = randint(1,100)
        y = randint(1,100)
        self.text = str(x)+self.op+str(y)
        if self.op == " + ":
            self.ans = x+y
        elif self.op == " - ":
            self.ans = x-y
        elif self.op == " * ":
            self.ans = x*y

    def check_correct(self, res):
        return res == self.ans

    def __repr__(self):
        return self.text


class Matrix(object):
    def __init__(self):
        self.array = [[0 for x in range(8)] for y in range(3)]
        '''
        array value correspondance:
        0: nothing
        1: ship, not hit
        2: nothing, hit
        3: ship, hit
        '''
        self.message = 0

    def update_on_attack(self, x, y):
        '''
        updates 2D array with values after receiving attack coords
        changes self.message to "Hit" or "Miss"
        '''
        self.array[y][x] += 2
        if self.array[y][x] > 3:
            self.array[y][x] -= 2 #preserves state when hit multiple times
        self.message = 1 if (self.array[y][x] % 2) else 0

    def get_message(self):
        return self.message

    def put_ship(self, ship, x, y):
        '''
        places ship onto array; validity is already checked for
        '''
        for i in range(x,x+ship.size+1):
            self.array[y][i]=1

    def read_from_string(self, string):
        '''
        takes as input 24-char string and updates the array accordingly
        '''
        for i in range(24):
            row = i // 8
            col = i % 8
            self.array[row][col] = int(string[i])-48

    def prepare_string(self):
        package = ""
        for i in self.array:
            for j in i:
                package+=str(j)
        return package

def is_valid(ship, matrix, x, y):
    if not (0<=x<=7-ship.size+1) or not (0<=y<3): #checks for valid range
        return False
    else:
        for i in range(x, x+ship.size): #checks for prior occupancy
            if matrix.array[y][i]==1:
                return False
        return True

global my_map
my_map= Matrix()
global enemy_map
enemy_map = Matrix()
global exitflag
exitflag = 0
