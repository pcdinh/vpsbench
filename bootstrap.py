#!/usr/bin/env python
import os
import sys

"""
Installing PostgreSQL for running the MySQL benchmarks
and Django test suite:

    apt-get install postgresql libdbd-pg-perl python-psycopg2 libreadline5-dev python-scipy

    su postgres -c "createuser -P testuser"

    su postgres -c psql template1
        CREATE DATABASE test OWNER testuser ENCODING 'UTF8';

    vi /etc/postgresql/8.3/main/pg_hba.conf
        local    all    testuser    md5

    /etc/init.d/postgresql-8.3 restart

"""

if __name__ == "__main__":
    if "--all" in sys.argv:
        d_dir = "django"
        if not os.path.isdir(d_dir):
            u = " http://code.djangoproject.com/svn/django/trunk/@10680"
            os.system("svn co %s %s" % (u, d_dir))

        m_dir = "mysql-5.1.34"
        if not os.path.isdir(m_dir):
            u = "http://downloads.mysql.com/archives/mysql-5.1/mysql-5.1.34.tar.gz"
            cmd = "wget %s && tar xzf %s.tar.gz && cd %s && ./configure " + \
                  "&& make && cd .. && patch -p0 -i %s.patch"
            os.system(cmd % (u, m_dir, m_dir, m_dir))

        u_dir = "unixbench-5.1.2"
        if not os.path.isdir(u_dir):
            u = "http://www.hermit.org/Linux/Benchmarking/unixbench-5.1.2.tar.gz"
            cmd = "wget %s && tar xzf %s.tar.gz && " + \
                  "patch -p0 -i %s.patch && cd %s && make all"
            os.system(cmd % (u, u_dir, u_dir, u_dir))

    g_dir = "GChartWrapper"
    if not os.path.isdir(g_dir):
        u = "http://google-chartwrapper.googlecode.com/svn/trunk/%s" % g_dir
        os.system("svn co %s" % u)
