#!/usr/bin/env python
import os

def echo_and_run(cmd):
    print "# %s" % cmd
    os.system(cmd)
    print ""

echo_and_run('uname -nrmo')
echo_and_run('grep "MemTotal" /proc/meminfo')
echo_and_run('grep -m 4 -e "model name" -e "MHz" -e "cache size" -e "bogomips" /proc/cpuinfo')
echo_and_run('grep "processor" /proc/cpuinfo | wc -l')
