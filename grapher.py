from __future__ import with_statement

import re

from glob import glob
from GChartWrapper import Line


def parse_benchmark_logs():
    results = {}
    host_re = re.compile("logs/([a-z.]+)-")
    django_re = re.compile("^Ran \d{3} tests in ([\d.]+)s")

    tests = [
        ('django_sqlite3_test', django_re),
        ('django_pgsql_test', django_re),
        ('pgsql_mysql_benchmark', re.compile("^TOTALS\s+([\d.]+)")),
        ('unix_benchmark', re.compile("Index Score\s+([\d.]+)")),
    ]

    for test in tests:
        test_name, test_re = test
        results[test_name] = {}
        for fname in sorted(glob("logs/*-%s.log" % test_name)):
            host = host_re.search(fname).group(1)
            results[test_name][host] = []
            with open(fname) as file:
                for line in file:
                    match = test_re.search(line)
                    if match:
                        results[test_name][host].append(float(match.group(1).split('.')[0]))

    results['unix_benchmark_single'] = {}
    results['unix_benchmark_multiple'] = {}
    for host, host_results in results['unix_benchmark'].items():
        results['unix_benchmark_single'][host] = []
        results['unix_benchmark_multiple'][host] = []
        for index, result in enumerate(host_results):
            if index % 2 == 0:
                results['unix_benchmark_single'][host].append(result)
            else:
                results['unix_benchmark_multiple'][host].append(result)
    
    del results['unix_benchmark']
    results['unix_benchmark_single']

    return results

def graph(data):
    hosts = (
        ('opal.redflavor.com', 'Slicehost'),
        ('garnet.redflavor.com', 'Prgmr'),
        ('topaz.redflavor.com', 'Linode'),
    )
    data = data['django_sqlite3_test']

    dataset = [data[host[0]] for host in hosts]

    g = Line(dataset, encoding='text')
    g.legend(*[host[1] for host in hosts])
    g.color("edc240", "afd8f8", "cb4b4b")
    g.size(550, 150)
    g.scale(150, 500)
    #g.show()
    print g



if __name__ == "__main__":
    graph(parse_benchmark_logs())
