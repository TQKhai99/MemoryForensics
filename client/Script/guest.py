import os
import subprocess
import time
import random
import psutil

# ABC
PATH = "Z:\\Script\\"
LIST_ACTION = "listaction.txt"
MODE = "mode.txt"
MALWARE_PATH = 'Z:\\malware\\'

def web(url):
    path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"        
    subprocess.Popen(path + " " + url)

def app(app):
    try:
        subprocess.Popen(app)
    except:
        pass


def main():
    result = []

    f = open(PATH + LIST_ACTION, 'r')
    for line in f:
        if '\t' not in line or 'internal log' in line:
            break
        if len(line) != 0:
            result.append(line.strip())
    f.close()

    for i in result:
        s = i.split('\t')
        if(s[0] == 'chrome'):
            web(s[1])
            time.sleep(2)
        if(s[0] == 'app'):
            app(s[1])
            time.sleep(2)
    time.sleep(5)

    fa = open(PATH + MODE)
    mode = fa.readline().splitlines()[0]
    name = fa.readline()

    if mode == "benign":
        for proc in psutil.process_iter():
            try:
                # Get process name & pid from process object.
                processName = proc.name()
                processID = proc.pid
                memorySize = proc.memory_info().vms / (1024*1024)
                if(memorySize > 0 and memorySize < 350):
                    os.system("Z:\\Procdump\\procdump.exe -ma " + str(processID))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    elif mode == "full":
        print("1")
    else:
        os.startfile(MALWARE_PATH + mode + '\\' + name)
        time.sleep(10)
        os.system("Z:\\Procdump\\procdump.exe -ma " + name)
    
if __name__ == '__main__':
    main()
