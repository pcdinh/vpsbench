#!/usr/bin/env python
from __future__ import with_statement

import re
from datetime import datetime, timedelta

from glob import glob
from GChartWrapper import Line


def parse_benchmark_logs():
    results = {}
    date_format = "%Y-%m-%d %H:%M:%S"
    date_re = re.compile("^Date: (.+)$")
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
                previous_date = None
                for line in file:
                    date_match = date_re.search(line)
                    if date_match:
                        date_str = date_match.group(1).split(".")[0]
                        previous_date = datetime.strptime(date_str,
                                                          date_format)
                    else:
                        match = test_re.search(line)
                        if match:
                            vals = (float(match.group(1)), previous_date,)
                            results[test_name][host].append(vals)

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

def graph(results):
    hosts = (
        ('opal.redflavor.com', 'Slicehost'),
        ('garnet.redflavor.com', 'Prgmr'),
        ('topaz.redflavor.com', 'Linode x86_64'),
        ('amethyst.redflavor.com', 'Linode i686'),
    )
    for test, data in results.items():
        datalist = [data[host[0]] for host in hosts]

        plots = []
        dates = []
        max_points = max([len(d) for d in datalist])
        for hostlist in datalist:
            hostplots = []
            hostdates = []
            for hostitem in hostlist:
                hostplots.append(hostitem[0])
                hostdates.append(hostitem[1])
            if len(hostplots) < max_points:
                hostplots.extend([0 for i in xrange(max_points-len(hostplots))])
            plots.append(hostplots)
            dates.append(hostdates)
        first_day = dates[0][0]
        last_day = dates[0][-1]
        delta = last_day - first_day
        diff = delta.days*60*60*24 + delta.seconds

        days = []
        days.append(first_day.strftime("%a"))
        days.append((first_day+timedelta(seconds=int(diff*0.2))).strftime("%a"))
        days.append((first_day+timedelta(seconds=int(diff*0.4))).strftime("%a"))
        days.append((first_day+timedelta(seconds=int(diff*0.6))).strftime("%a"))
        days.append((first_day+timedelta(seconds=int(diff*0.8))).strftime("%a"))
        days.append(last_day.strftime("%a"))

        maximum = int(max([max(d) for d in plots])) + 10
        minimum = int(min([min(d) for d in plots])) - 10

        g = Line(plots, encoding='text')
        g.legend(*[host[1] for host in hosts])
        g.legend_pos('b')
        g.color("edc240", "afd8f8", "cb4b4b", "4da74d")
        for i in range(3):
            g.line(2.5, 1, 0)
        g.size(500, 200)
        g.scale(minimum, maximum)
        g.axes.type('xy')
        labels = range(minimum, maximum, (maximum-minimum)/5)
        g.axes.label(0, *days)
        g.axes.label(1, *labels)
        #g.show()
        print "%s:\n%s\n" % (test, g)



if __name__ == "__main__":
    graph(parse_benchmark_logs())
