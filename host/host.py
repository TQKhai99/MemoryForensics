import argparse
import os
import sys
import time
import random
from os import listdir

PROCESS_COUNT_MIN = 15
PROCESS_COUNT_MAX = 20
FILES_PATH = '/home/r0n/Desktop/memdump/files/'
DUMP_PATH = '/home/r0n/Desktop/memdump/dump/'
LIST_ACTION = '/media/r0n/My Passport/Virtual/Script/listaction.txt'
MODE = '/media/r0n/My Passport/Virtual/Script/mode.txt'
MALWARE_PATH = '/media/r0n/My Passport/Virtual/malware/'
MACHINE_ID = 'TEST'
web_list = []
app_list = []
app_win_list = []

def add_action(line):
    # Add action to list
    file = open(LIST_ACTION, 'a')
    file.write(str(line) + '\n')
    file.close()

def web():
    # Add web
    website = random.sample(web_list, 1)[0]
    line = "chrome" + '\t' + website
    add_action(line)

def app(process_type):
    # Add app
    if process_type == 'app':
        app = random.sample(app_list,1)[0]
    elif process_type == 'app_win':
        app = random.sample(app_win_list,1)[0]
    line = 'app\t' + app
    add_action(line)

def load_actions():
    #Load domains
    f = open(FILES_PATH + 'domain.txt','r')
    for line in f:
        line = line.strip()
        if len(line) == 0:
            break
        line = 'https://www.' + line
        web_list.append(line)
    f.close()
    #Load app
    f = open(FILES_PATH + 'app.txt','r')
    for line in f:
        line = line.strip()
        if len(line) == 0:
            break
        s = line.split('\t')
        app_list.append(s[1])
    f.close()
    #Load app windows
    f = open(FILES_PATH + 'app_windows.txt','r')
    for line in f:
        line = line.strip()
        if len(line) == 0:
            break
        s = line.split('\t')
        app_win_list.append(s[1])
    f.close()

def load_malware(malware):
    global malwares
    malwares = os.listdir(MALWARE_PATH + malware + '/')

def mode(mode, number):
    # Random version malware
    file = open(MODE, 'w')
    file.write(str(mode) + '\n')
    if mode != "benign" and mode != "full":
        file.write(str(malwares[number]))

def random_process():
    return random.sample(['chrome', 'app', 'app_win'], 1)[0]

def clear_file():
    file = open(LIST_ACTION, 'w')
    file.write("")
    file.close()

def main(argv=None):

    parser = argparse.ArgumentParser(description="MemGen! A tool used to generate dump of malware or benign or whole memory!")
    parser.add_argument('file', type=argparse.FileType("rb"), default=sys.stdin,
                        help="host.py")
    parser.add_argument("-m", "--mode", type=str, default=None,
                        help="benign or name of malware or full (to dump whole memory))")
    parser.add_argument("-q", "--quantity", type=int, default=None,
                        help="quantity you want (default = 1)")
    if argv is None:
        argv = sys.argv
    args = parser.parse_args(argv)
    if args.mode is None:
        args.mode = "benign"
    if args.quantity is None:
        args.quantity = 1
    load_actions()
    if args.mode != "benign" and args.mode != "full":
        load_malware(args.mode)
    for image_count in range(args.quantity):
        print(str(image_count) + '  ======================================')
        os.system('date')
        clear_file()
        print('Generating random actions.')
        PROCESS_COUNT = random.randint(PROCESS_COUNT_MIN, PROCESS_COUNT_MAX)
        for process in range(PROCESS_COUNT):
            type = random_process()
            if type == 'chrome':
                web()
            if type == 'app' or type == 'app_win':
                app(type)
        if args.mode == "benign" or args.mode == "full":
            mode(args.mode, 1)
        else:
            mode(args.mode ,image_count % len(malwares))
        os.system('VBoxManage snapshot ' + MACHINE_ID + ' restore snapshot')
        os.system('VBoxManage startvm ' + MACHINE_ID + ' --type headless')
        if args.mode == "benign":
            time.sleep(300)
        elif args.mode == "full":
            time.sleep(100)
            os.system("vboxmanage debugvm " + MACHINE_ID + " dumpvmcore --filename " + str(image_count) + ".elf")
            os.system("sh tomemdump.sh " + str(image_count))
            time.sleep(20)
        else:
            time.sleep(135)
        os.system('VBoxManage controlvm ' + MACHINE_ID + ' poweroff')
        print('VM closed.')
        time.sleep(3)
        

if __name__ == '__main__':
    main()
