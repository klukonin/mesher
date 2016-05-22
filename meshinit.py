#!/usr/bin/env python

import pexpect
import sys
import re
import getpass
from StringIO import StringIO

# Try to connect
try:
    hostname = raw_input('hostname:')
    ssh = pexpect.spawn ('ssh root@' + hostname )
    password = getpass.getpass('password:')
    ssh.expect ('yes/no')
    ssh.sendline ('yes')
    ssh.expect ('assword')
    ssh.sendline (password)
    ssh.expect ('#')
except
    print("Failed to connect. Please check hostname or authentication credentials")

# Configuration of internet access and mesh installation
try:
    ssh.sendline('opkg remove wpad-mini')
    ssh.promt('#')
    gateway = raw_input('internet gateway:')
    ssh.sendline ('route add default gw ' + gateway)
    dns = raw_input('internet DNS:')
    ssh.sendline ('echo “nameserver'+ dns + '”'+' >> /etc/resolv.conf')
    ssh.sendline('opkg update')
    ssh.promt ('#')
    ssh.sendline('opkg install --force-depends batctl wpad python')
except
    print ('Sorry, no internet access')

#Configurating mesh and download a script    
try:
  ssh.sendline('mkdir /usr/share/optimizer')
  ssh.promt ('#')
  ssh.sendline('cd /tmp')
  ssh.promt ('#')
  ssh.sendline ('wget http://raw.githubusercontent.com/klukonin/mesher/master/mesherd')
  ssh.promt ('#')
  ssh.sendline ('wget http://raw.githubusercontent.com/klukonin/mesher/master/mesher.py')
  ssh.promt ('#')# адрес файла
  ssh.sendline ('mv mesher.py /usr/share/optimizer')
  ssh.promt ('#')
  ssh.sendline ('mv mesherd /')
  ssh.promt ('#')
  
  
    

    
