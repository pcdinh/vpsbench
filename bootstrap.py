import os

if __name__ == "__main__":
    d_dir = "django"
    if not os.path.isdir(d_dir):
        u = " http://code.djangoproject.com/svn/django/trunk/@10680"
        os.system("svn co %s %s" % (u, d_dir))

    ub_dir = "unixbench-5.1.2"
    if not os.path.isdir(ub_dir):
        u = "http://www.hermit.org/Linux/Benchmarking/unixbench-5.1.2.tar.gz"
        cmd = "wget %s && tar xzf %s.tar.gz && cd %s && " + \
              "sed 's/\(GRAPHIC_TESTS\)/#\\1/ ' Makefile > mk.tmp && " + \
              "mv mk.tmp Makefile && make"
        os.system(cmd % (u, ub_dir, ub_dir))

    pg_dir = "postgresql-8.3.7"
    if not os.path.isdir(pg_dir):
        u = "http://ftp9.us.postgresql.org/pub/mirrors/postgresql/" + \
            "source/v8.3.7/postgresql-8.3.7.tar.gz"
        cmd = "wget %s && tar xzf %s.tar.gz && cd %s && ./configure && " + \
              "make"
        os.system(cmd % (u, pg_dir, pg_dir))
