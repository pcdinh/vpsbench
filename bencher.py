from __future__ import with_statement

import os
import time
import subprocess

from datetime import datetime as dt
from datetime import timedelta
from socket import gethostname

HOST = gethostname()

def run(command):
    proc = subprocess.Popen(command,
                            shell=True,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    return "\n".join(proc.communicate())

def write_log(fname, data, number):
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    path = "logs/%s-%s.log" % (HOST, fname)
    with open(path, 'a') as f:
        f.write("\n\nRun: %s\nDate: %s\n\n" % (number, dt.now()))
        f.write(data)
    os.system("git add %s" % path)


if __name__ == "__main__":
    test_dir = './django/tests'
    python_path = "export PYTHONPATH=django:."
    d_cmd_template = "%s && time %s/runtests.py --settings=" % (python_path,
                                                               test_dir)
    d_cmd = lambda setting: "%s%s" % (d_cmd_template, setting)

    usr = "testuser"
    pwd = "n0ns3curepWd"
    tests = "time ./run-all-tests --silent --force " + \
            "--server=Pg --user=%s --password=%s" % (usr, pwd)
    p_cmd = "cd mysql-5.1.34/sql-bench && %s" % tests

    u_cmd = "cd unixbench-5.1.2 && time ./Run"

    start = dt.now()
    for i in range(1, 10000):
        print "Running %s" % i

        write_log('django_sqlite3_test', run(d_cmd("sqlite3conf")), i)
        time.sleep(60*5)
        write_log('django_pgsql_test', run(d_cmd("pgsqlconf")), i)
        time.sleep(60*5)
        write_log('pgsql_mysql_benchmark', run(p_cmd), i)
        time.sleep(60*5)
        write_log('unix_benchmark', run(u_cmd), i)

        os.system('git pull')
        os.system('git commit -m "Logging run %s (%s)"' % (i, HOST))
        os.system('git push')

        while dt.now() - start < timedelta(hours=3):
            time.sleep(10)
        start = dt.now()
