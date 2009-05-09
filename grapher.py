from __future__ import with_statement

import re

from glob import glob

def parse_benchmark_logs():
    results = {}
    host_re = re.compile("logs/([a-z.]+)-")
    django_re = re.compile("^Ran \d{3} tests in ([\d.]+)s")

    tests = [
        ('django_sqlite3_test', django_re),
        ('django_pgsql_test', django_re),
        ('pgsql_mysql_benchmark', re.compile("^TOTALS\s+([\d.]+)")),
    ]

    for test in tests:
        test_name, test_re = test
        results[test_name] = {}
        for fname in sorted(glob("logs/*-%s.log" % test_name)):
            host = host_re.search(fname).group(1)
            results[test_name][host] = []
            with open(fname) as file:
                for line in file:
                    match = test_re.match(line)
                    if match:
                        results[test_name][host].append(match.group(1))

    return results

if __name__ == "__main__":
    print parse_benchmark_logs()
