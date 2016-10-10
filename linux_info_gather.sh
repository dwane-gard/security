#!/bin/sh

echo Distrubtuib and kernel version

cat /etc/issue
uname -a

echo Mounted File System
mount -l

echo Network Configuration
ifconfig -a
cat /etc/hosts
arp

echo Development Tools availability
which gcc
which g++
which python

echo Installed  packages (debian derivitive)
dpkg -l

echo Services
netstat -tulnpe

echo Processses
ps -aux

echo Scheduled jobs
find /etc/cron* -ls 2>/dev/null
find /var/spool/cron* -ls 2>/dev/null

echo readable files in /etc/
find /etc -user 'id -u' -erpm -u=r \
	-o -group 'id -g' =er, -g=r \
	-o -perm -o=r \
	-ls 2>/dev/null

echo SUID and GUID writable files
find / -o group 'id -g' -perm -g=w -perm -u=s \
	-o -perm -o=w -perm -u=s \
	-p -perm -o=w -perm -g=s \
	-ls 2>/dev/null

echo suid and guid files
find / -type f -perm -u=s -o -type f -perm -g=s \
	-ls 2>/dev/null


echo writable files outside HOME
mount -l find / -path "$HOME" -prube -o -path "/proc" -prune -o \( ~ -type l
\) \( -user 'id -u' -perm -u=w -o -group 'id -g' -perm -g=w -o -perm -o=w
\) -ls 2>/dev/null


