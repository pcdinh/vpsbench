from __future__ import with_statement

import time
import subprocess

from datetime import datetime as dt

def run(command):
    proc = subprocess.Popen(command,
                            shell=True,
                            stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    return "\n".join(proc.communicate())

def write_log(fname, data, number):
    with open(fname, 'a') as f:
        f.write("\n\nRun: %s\nDate: %s\n\n" % (number, dt.now()))
        f.write(data)


if __name__ == "__main__":
    test_dir = './django/tests'
    python_path = "export PYTHONPATH=django:."
    d_cmd = "%s && time %s/runtests.py --settings=sqlite3conf model_forms" % (python_path,
                                                                  test_dir)
    u_cmd = "cd unixbench-5.1.2 && time ./Run"

    p_cmd = "cd postgresql-8.3.7 && time make check"

    now = dt.now()
    for i in range(1, 10000):
        print "Running %s" % i
        write_log('django_test.log', run(d_cmd), i)

        #time.sleep(60*5)
        #write_log('unixbench.log', run(u_cmd), i)
        #time.sleep(60*5)
        write_log('postgresql_regression.log', run(p_cmd), i)
        

        while now.hour == dt.now().hour:
            time.sleep(60)
        now = dt.now()
