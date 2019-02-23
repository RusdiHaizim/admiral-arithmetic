class Ship(object):
    def __init__(self, name, size):
        self.name = name
        self.size = size

    def get_name(self):
        return self.name

class Question(object):
    def __init__(self,operation):
        self.op = " "+operation+" "
        x = randint(100)
        y = randint(100)
        self.text = str(x)+self.op+str(y)
        if self.op == " + ":
            self.ans = x+y
        elif self.op == " - ":
            self.and = x-y
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
        self.array[x][y] += 2
        self.message = 1 if (self.array[x][y] % 2) else self.message = 0

    def get_message(self):
        return self.message

    def put_ship(self, ship, x, y):
        '''
        places ship onto array; validity is already checked for
        '''
        for i in range(x,x+ship.size+1):
            self.array[i][y]=1

    def read_from_string(self, string):
        '''
        takes as input 24-char string and updates the array accordingly
        '''
        for i in range(24):
            row = i // 8
            col = i % 8
            self.array[row][col] = int(string[i])

    def prepare_string(self):
        package = ""
        for i in self.array:
            for j in i:
                package.append(str(j))
        return package

def is_valid(ship, matrix, x, y):
    if !(0<=x<=7-ship.size+1) or !(0<=y<=3): #checks for valid range
        return False
    else:
        for i in range(x, x+ship.size): #checks for prior occupancy
            if matrix.array[i][y]==1:
                return False
        return True
