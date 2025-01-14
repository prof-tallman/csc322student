import curses
from threading import Thread
from playsound import playsound
from datetime import datetime


turntable_rotating = False
def rotate_machine(mode):
    global turntable_rotating
    turntable_rotating = True
    playsound('whirring.wav')
    turntable_rotating = False
    return

def configure_xray_mode():
    t = Thread(target=rotate_machine, args=['XRAY'])
    t.start()

def configure_electron_mode():
    t = Thread(target=rotate_machine, args=['ELECTRON'])
    t.start()


cur_pos = [(1,16), (2,41), (2,64), (5,50), (6,50), (7,50),
           (10,50), (11,50), (12,50), (13,50), (14,50), (15,50),
           (22, 59)]
cur_min = [16, 41, 64, 50, 50, 50, 50, 50, 50, 50, 50, 50, 59]
cur_max = [40, 41, 70, 60, 60, 60, 60, 60, 60, 60, 60, 60, 59]
patient = ['  0.000000', '210.000000', '  0.350000', '  0.000000', 
           '348.200000', ' 15.300000', ' 27.600000', '  1.000000',
           '  0.000000']
verified_x = 70

def draw_menu(win):
    win.box(0, 0)
    win.addstr(1, 2, 'PATIENT NAME: ')
    win.addstr(2, 2, 'TREATMENT MODE: FIX')
    win.addstr(2, 30, 'BEAM TYPE: ')
    win.addstr(2, 50, 'ENERGY (KeV): ')
    win.addstr(4, 30, 'ACTUAL')
    win.addstr(4, 50, 'PRESCRIBED')
    win.addstr(5, 9, 'UNIT RATE/MINUTE')
    win.addstr(5, 30, patient[0])
    win.addstr(6, 9, 'MONITOR UNITS')
    win.addstr(6, 30, patient[1])
    win.addstr(7, 9, 'TIME(MIN)')
    win.addstr(7, 30, patient[2])
    win.addstr(10, 2, 'GANTRY ROTATION (DEG)')
    win.addstr(10, 30, patient[3])
    win.addstr(11, 2, 'COLLIMATOR ROTATION (DEG)')
    win.addstr(11, 30, patient[4])
    win.addstr(12, 2, 'COLLIMATOR X (CM)')
    win.addstr(12, 30, patient[5])
    win.addstr(13, 2, 'COLLIMATOR Y (CM)')
    win.addstr(13, 30, patient[6])
    win.addstr(14, 2, 'WEDGE NUMBER')
    win.addstr(14, 30, patient[7])
    win.addstr(15, 2, 'ACCESSORY NUMBER')
    win.addstr(15, 30, patient[8])
    win.addstr(20, 2, 'DATE:')
    win.addstr(20, 24, 'SYSTEM: BEAM READY')
    win.addstr(20, 50, 'OP.MODE: TREAT')
    win.addstr(20, 72, 'AUTO')
    win.addstr(21, 2, 'TIME:')
    win.addstr(21, 24, 'TREAT: TREAT PAUSE')
    win.addstr(21, 59, 'XRAY')
    win.addstr(21, 72, '013370')
    win.addstr(22, 2, 'OPR ID: PROF-TALLMAN')
    win.addstr(22, 24, 'REASON: OPERATOR')
    win.addstr(22, 50, 'COMMAND:')
    return

def update_time(win):
    current_time = datetime.now()
    win.addstr(20, 8, f'{current_time:%Y-%m-%d}')
    win.addstr(21, 8, f'{current_time:%H:%M:%S}')

def main(screen):

    curses.start_color()
    win = curses.newwin(24, 80, 0, 0)

    height, width = win.getmaxyx()

    key = 0
    cur_x = 0
    cur_y = 0
    cur_idx = 0
    value = ''

    draw_menu(win)
    cur_y, cur_x = cur_pos[cur_idx]
    win.move(cur_y, cur_x)

    while chr(key) != 'q' and chr(key) != 'Q':

        update_time(win)
        if (key >= ord('a') and key <= ord('z') or
                key >= ord('A') and key <= ord('Z') or
                key >= ord('0') and key <= ord('9') or
                key == ord('.') or key == ord(' ')):
            key = chr(key)
            if cur_idx == 1:
                key = key.upper()
                if key == 'X':
                    screen.addch(cur_y, cur_x, key)
                    configure_xray_mode()
                elif key == 'E':
                    screen.addch(cur_y, cur_x, key)
                    configure_electron_mode()
            if cur_idx >= 3 and cur_idx < len(cur_pos)-1:
                if key >= '0' and key <= '9' or key == '.':
                    screen.addch(cur_y, cur_x, key)
                    value += key
            elif cur_idx == len(cur_pos)-1:
                key = key.upper()
                if key == 'P':
                    screen.addch(cur_y, cur_x, key)
                    if turntable_rotating:
                        playsound('scream.wav')
                    else:
                        playsound('success.wav')
            else:
                screen.addch(cur_y, cur_x, key)
            if cur_x < cur_max[cur_idx]:
                cur_x += 1

        #elif :
         #   cur_idx = len(cur_pos)-1
          #  cur_y, cur_x = cur_pos[cur_idx]


        elif key == curses.KEY_BACKSPACE or key == 127:
            if cur_x > cur_min[cur_idx]:
                cur_x -= 1

        elif (key == curses.KEY_DOWN or key == curses.KEY_RIGHT or
              key == curses.KEY_ENTER or key == 10):
            if cur_idx >= 3 and cur_idx < len(cur_pos)-1:
                value = value.strip()
                #if float(value) == float(patient[cur_idx-3]):
                win.addstr(cur_y, verified_x, 'VERIFIED')
            cur_idx = min(cur_idx + 1, len(cur_pos)-1)
            cur_y, cur_x = cur_pos[cur_idx]
            value = ''

        elif key == curses.KEY_UP or key == curses.KEY_LEFT:
            cur_idx = max(cur_idx - 1, 0)
            cur_y, cur_x = cur_pos[cur_idx]
            value = ''

        win.move(cur_y, cur_x)
        win.refresh()
        key = screen.getch()

    curses.endwin()

#print("Preparing to initialize screen...")
#input("Press <ENTER> to begin")

screen = curses.initscr()
print("Screen initialized.")
curses.wrapper(main)

print("Window ended.")



'''
screen.clear()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
screen.addstr("Regular text\n")
screen.addstr("Bold\n", curses.A_BOLD)
screen.addstr("Highlighted\n", curses.A_STANDOUT)
screen.addstr("Underline\n", curses.A_UNDERLINE)
screen.addstr("Regular text again\n")
screen.addstr("RED ALERT!\n", curses.color_pair(1))
screen.addstr("SUPER RED ALERT!\n", curses.color_pair(1) | curses.A_BOLD | curses.A_UNDERLINE)
screen.refresh()
c = screen.getch()

screen.addstr(f"You pressed {chr(c)}\n", curses.color_pair(1))
screen.refresh()
'''