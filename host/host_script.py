import os
import sys
import time
import random
from os import listdir

IMAGE_COUNT = 100
PROCESS_COUNT_MIN = 15
PROCESS_COUNT_MAX = 20
FILES_PATH = '/home/r0n/Desktop/memdump/files/'
DUMP_PATH = '/home/r0n/Desktop/memdump/dump/'
SAMPLE = '/media/r0n/My Passport/Virtual/Script/sample_Win10.txt'
web_list = []
app_list = []
app_win_list = []
malware = []

def add_action(action_list_file, line):
    #print line
    file = open(action_list_file, 'a')
    file.write(str(line) + '\n')
    file.close()

def add_web(action_list_file):
    website = random.sample(web_list, 1)[0]
    line = "chrome" + '\t' + website
    add_action(action_list_file, line)

def add_app(action_list_file, process_type):
    if process_type == 'app':
        app = random.sample(app_list,1)[0]
    elif process_type == 'app_win':
        app = random.sample(app_win_list,1)[0]
    line = 'app\t' + app
    add_action(action_list_file, line)

def random_process_type():
    return random.sample(['web'], 1)[0]

def load_all_actions():
    f = open(FILES_PATH + 'domain.txt','r')
    for line in f:
        line = line.strip()
        if len(line) == 0:
            break
        line = 'https://www.' + line
        web_list.append(line)
    f.close()
    f = open(FILES_PATH + 'app.txt','r')
    for line in f:
        line = line.strip()
        if len(line) == 0:
            break
        s = line.split('\t')
        app_list.append(s[1])
    f.close()
    f = open(FILES_PATH + 'app_windows.txt','r')
    for line in f:
        line = line.strip()
        if len(line) == 0:
            break
        s = line.split('\t')
        app_win_list.append(s[1])
    f.close()
    f = open(FILES_PATH + 'malware.txt','r')
    for line in f:
        if len(line) == 0:
            break
        malware.append(line)
    f.close()


def random_process_type():
    return random.sample(['chrome', 'app', 'app_win'], 1)[0]

def clear_file():
    file = open(SAMPLE, 'w')
    file.write("")
    file.close()

def main():
    machine_id = 'TEST'
    action_list_file = SAMPLE
    load_all_actions()
    for image_count in range(IMAGE_COUNT):
        print(str(image_count) + '  ======================================')
        os.system('date')
        clear_file()
        print 'Generating random actions.'
        PROCESS_COUNT = random.randint(PROCESS_COUNT_MIN, PROCESS_COUNT_MAX)
        for process_count in range(PROCESS_COUNT):
            process_type = random_process_type()
            if process_type == 'chrome':
                add_web(action_list_file)
            if process_type == 'app' or process_type == 'app_win':
                add_app(action_list_file, process_type)
        os.system('VBoxManage snapshot ' + machine_id + ' restore snapshot')
        os.system('VBoxManage startvm ' + machine_id + ' --type gui')
        time.sleep(135)
        os.system('VBoxManage controlvm ' + machine_id + ' poweroff')
        print('VM closed.')
        time.sleep(3)
    

if __name__ == '__main__':
    main()
