import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

player_map = [[0]*8]*3
hit_map = player_map.copy()
empty = player_map.copy()

green_row_lst = [35,36,37]
red_row_lst = [31,32,33]
column_lst = [3,5,7,8,10,11,12,13]

for i in column_lst: # set all pins to output
    GPIO.setup(i, GPIO.OUT)
for i in red_row_lst: # set all pins to output
    GPIO.setup(i, GPIO.OUT)
for i in green_row_lst: # set all pins to output
    GPIO.setup(i, GPIO.OUT)

for i in column_lst:
    GPIO.output(i, True)

for j in green_row_lst:
    GPIO.output(j, False)

for k in red_row_lst:
    GPIO.output(k, False)

GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

time_stamp = time.time()
turn = 0
flag = True

def show_all(): # show player's hit map
    off_all()
    time.sleep(0.1)
    update_display(mtostr(hit_map))

def off_all():
    update_display(mtostr(empty))
            
def led_on(x, y, colour):
    GPIO.output(column_lst[y], False)
    if colour == 1:
        GPIO.output(green_row_lst[x], True)
    elif colour == 3:
        GPIO.output(red_row_lst[x], True)
    time.sleep(0.1)
    led_off(x, y, colour)

def led_off(x, y, colour):
    GPIO.output(column_lst[y], True)
    if colour == 1:
        GPIO.output(green_row_lst[x], False)
    elif colour == 3:
        GPIO.output(red_row_lst[x], False)
    
def my_callback(channel):
    global time_stamp
    global turn
    global flag
    time_now = time.time()
    if (time_now - time_stamp) >= 0.3:
        turn = 1 - turn
        if turn:
            flag = False
            show_all()
            print("Flag is false")
        elif turn == 0:
            off_all()
            flag = True
            print("Flag is true")
            #return
    print("Turn is")
    print(turn)
    time_stamp = time_now
    update_display(player_map)

GPIO.add_event_detect(16, GPIO.BOTH, callback=my_callback)

def mtostr(m):
    string = ""
    for i in range(len(m)):
        for j in range(len(m[i])):
            string += str(m[i][j])
    return string

def constructm(string):
    matrix = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

    for i in range(24):
        matrix[i // 8][i % 8] = int(string[i])
    return matrix

def update_display(string):
    matrix = constructm(string)

    for i in range(3):
        for j in range(8):
            led_on(i,j,matrix[i][j])
    
    
