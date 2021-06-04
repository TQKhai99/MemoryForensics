import os
import subprocess
import time
import random
# ABC
PATH = "Z:\\Script\\"
LIST_NAME = "sample_Win10.txt"
MALWARE = "malware.txt"
MALWARE_PATH = 'Z:\\malware\\'

def open_web(app, url):
    if  app == 'chrome':
        path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"        
    subprocess.Popen(path + " " + url)

def open_app(app):
    try:
        subprocess.Popen(app)
    except:
        print app


def main():
    result = []
    f = open(PATH + LIST_NAME, 'r')
    for line in f:
        if '\t' not in line or 'internal log' in line:
            break
        if len(line) != 0:
            result.append(line.strip())
    f.close()
    for i in result:
        s = i.split('\t')
        if(s[0] == 'chrome'):
            open_web(s[0], s[1])
            time.sleep(2)
        if(s[0] == 'app'):
            open_app(s[1])
            time.sleep(2)
    time.sleep(10)
    fa = open(PATH + MALWARE)
    file = fa.readline().splitlines()[0]
    name = fa.readline()
    os.startfile(MALWARE_PATH + file + '\\' + name)
    time.sleep(10)
    os.system("Z:\\Procdump\\procdump.exe -ma " + name)
    
main()
