#!/usr/bin/env python3
import socket
import time
import os
from gi.repository import Notify

#Port checking tool.
def DoesServiceExist(host, port):
    captive_dns_addr = ""
    host_addr = ""

    try:
        host_addr = socket.gethostbyname(host)

        if (captive_dns_addr == host_addr):
            return False

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((host, port))
        s.close()
    except:
        return False
    return True

#Test if a server is open.
def testOpen(homeDir):
    try:
        serverList = open(homeDir + '/.scheckrc', 'r')
        for servers in serverList:
            serverSplit = servers.split()
            serverName = serverSplit[0]
            serverPort = serverSplit[1]
            Notify.init(serverName)
            print("Testing server %s on port %s" % (serverName, serverPort))
            if (DoesServiceExist(serverName, int(serverPort))):
                print('Server is up.')
                serverNotice=Notify.Notification.new (serverName, 'Server is up!', 'dialog-information')
                serverNotice.show()
            else:
                print('Server is down.')
                serverNotice=Notify.Notification.new (serverName, 'Server is down!', 'dialog-information')
                serverNotice.show()
        return True
    except:
        print('An error has occured. Please check your ~/.scheckrc file.')
        return False

def main():
    #Repeats the check function.
    homeDir = os.getenv("HOME")
    if homeDir != None:
        returnOpen = testOpen(homeDir)
        while returnOpen != False:
            #Sleep time in seconds.
            try:
                SleepTime = 5 * 60
                time.sleep(SleepTime)
                returnOpen = testOpen()
            except:
                print('Ending.')
                returnOpen = False
        return True
    else:
        return False
        
if __name__ == '__main__':
    quit(main())
