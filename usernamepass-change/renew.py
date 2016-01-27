#!/usr/bin/env python
'''
for change sysname and password 
write by liwei 20151221
'''

import warnings
warnings.filterwarnings("ignore")


import paramiko
import sys

def help():
	print '\033[1;31;40m'
	print '*' * 50
	print '\neg: python renew.py -repass/-rename $/hosttext \n\n1, Use -repass to change password \n------hosttext form : ip sshport user oldpass newpass\nfor exemple :\n192.168.1.2 22 root 000000 123456\n15.80.193.1 22 cacti 123456 000\n\n2, Use -rename to change username \n------hosttext form : ip sshport username\nfor exemple:\n192.168.1.2 22 PR-DL-1.3\n15.80.193.1 22 SABER\n\n'
	print '*' * 50
	print '\033[0m'

'''
change password
'''
def repass(ip,port,user,oldpass,newpass):
	try:
		ssh =paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(ip,port,'root',oldpass,timeout=5)
		cmd = 'echo %s | passwd --stdin %s'%(newpass,user)
		stdin, stdout, stderr = ssh.exec_command(cmd)
		stdin.write("Y")
		ssh.close()
	except :
        	print '%s\tError\n'%(ip)

'''
change sysname
'''
def rename(ip,port,name,passwd):
	try:
                ssh =paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip,port,'root',passwd,timeout=5)
                cmd = 'sed -i "/^127.0.0.1/c 127.0.0.1   localhost %s localhost4 localhost4.localdomain4" /etc/hosts'%(name)
		stdin, stdout, stderr = ssh.exec_command(cmd)
                stdin.write("Y")
		cmd1 = 'sed -i "/^HOSTNAME/c HOSTNAME=%s" /etc/sysconfig/network'%(name)
		stdin, stdout, stderr = ssh.exec_command(cmd1)
                stdin.write("Y")
		stdin, stdout, stderr = ssh.exec_command('hostname %s'%name)
		stdin.write("Y")
                ssh.close()
        except :
                print '%s\tError\n'%(ip)

if __name__ == '__main__':
	try:
		if sys.argv[1] == '-repass':
			file = open(sys.argv[2],'r')
			i = 0
			f = file.readline().strip()
			while i < len(f):
				elem = f.split()
				ip,port,user,oldpass,newpass = elem
				repass(ip,int(port),user,oldpass,newpass)
				f = file.readline().strip()
				i = i + 1
			file.close()
		elif sys.argv[1] == '-rename':
			file = open(sys.argv[2],'r')
                        i = 0
                        f = file.readline().strip()
                        while i < len(f):
                                elem = f.split()
                                ip,port,passwd,name = elem
                                rename(ip,int(port),name,passwd)
                                f = file.readline().strip()
                                i = i + 1
			file.close()
		else:
			help()	
	except:
		help()		
