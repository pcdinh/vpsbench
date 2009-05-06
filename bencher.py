from __future__ import with_statement

import os
import time
import subprocess

from datetime import datetime as dt
from socket import gethostname

def run(command):
    proc = subprocess.Popen(command,
                            shell=True,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    return "\n".join(proc.communicate())

def write_log(fname, data, number):
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    path = "logs/%s%s.log" % (gethostname(), fname)
    with open(path, 'a') as f:
        f.write("\n\nRun: %s\nDate: %s\n\n" % (number, dt.now()))
        f.write(data)


if __name__ == "__main__":
    test_dir = './django/tests'
    python_path = "export PYTHONPATH=django:."
    d_cmd = "%s && time %s/runtests.py --settings=sqlite3conf" % (python_path,
                                                                  test_dir)
    usr = "testuser"
    pwd = "n0ns3curepWd"
    tests = "time ./run-all-tests --silent --small-test " + \
            "--server=Pg --user=%s --password=%s" % (usr, pwd)
    p_cmd = "cd mysql-5.1.34/sql-bench && %s" % tests

    now = dt.now()
    for i in range(1, 10000):
        print "Running %s" % i

        write_log('django_test', run(d_cmd), i)
        time.sleep(60*5)
        write_log('pgsql_mysql_benchmark', run(p_cmd), i)

        while now.hour == dt.now().hour:
            time.sleep(60)
        now = dt.now()
