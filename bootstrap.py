import os

"""
Installing PostgreSQL for running the MySQL benchmarks:

    apt-get install postgresql libdbd-pg-perl

    su postgres -c "createuser -P testuser"

    su postgres -c psql template1
        CREATE DATABASE test OWNER testuser ENCODING 'UTF8';

    vi /etc/postgresql/8.3/main/pg_hba.conf
        local    test    testuser    md5

    /etc/init.d/postgresql-8.3 restart

"""

if __name__ == "__main__":
    d_dir = "django"
    if not os.path.isdir(d_dir):
        u = " http://code.djangoproject.com/svn/django/trunk/@10680"
        os.system("svn co %s %s" % (u, d_dir))

    m_dir = "mysql-5.1.34"
    if not os.path.isdir(m_dir):
        u = "http://mysql.he.net/Downloads/MySQL-5.1/mysql-5.1.34.tar.gz"
        cmd = "wget %s && tar xzf %s.tar.gz && cd %s && ./configure && " + \
              "make"
        os.system(cmd % (u, m_dir, m_dir))
