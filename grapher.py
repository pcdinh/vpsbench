#!/usr/bin/env python
from __future__ import with_statement

import re
from datetime import datetime, timedelta

import numpy
from glob import glob
from GChartWrapper import Line

HOSTS = (
    ('opal.redflavor.com', 'Slicehost'),
    ('garnet.redflavor.com', 'Prgmr'),
    ('topaz.redflavor.com', 'Linode x86_64'),
    ('amethyst.redflavor.com', 'Linode i686'),
    ('onyx.redflavor.com', 'Amazon'),
    ('beryl.redflavor.com', 'Rackspace'),
)

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
    output = []
    sorted_keys = results.keys()
    sorted_keys.sort()
    for test in sorted_keys:
        data = results[test]
        datalist = [data[host[0]] for host in HOSTS]

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
                hostplots.extend([hostlist[-1][0] for i in xrange(max_points-len(hostplots))])
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

        maximum = max([max(d) for d in plots])
        minimum = min([min(d) for d in plots])

        def scale(value, scale=4095):
            return (value - minimum) * scale / abs(maximum - minimum)

        scaled_plots = []
        for hostplots in plots:
            scaled_plots.append([scale(v) for v in hostplots])

        g = Line(scaled_plots, encoding='extended')
        g.legend(*[host[1] for host in HOSTS])
        g.legend_pos('b')
        g.color("edc240", "afd8f8", "cb4b4b", "4da74d", "f8afe8", "4066ed", )
        for i in range(3):
            g.line(2.5, 1, 0)
        g.size(500, 300)
        #g.scale(minimum, maximum)
        g.axes.type('xy')
        labels = range(minimum, maximum, (maximum-minimum)/5)
        g.axes.label(0, *days)
        g.axes.label(1, *labels)
        #g.show()
        print test
        print g
        output.append("%s" % g)
    #print ", ".join(output)

def style(index, value, test, dataset):
    values = []
    for host in HOSTS:
        hostkey, hostname = host
        values.append(dataset[hostkey][test][index])
    maxmatch = max(values) == value
    minmatch = min(values) == value
    if index == 0:
        if "unix_" in test:
            if maxmatch:
                return "background: #e6efc2;"
            if minmatch:
                return "background: #fbe3e4;"
        else:
            if maxmatch:
                return "background: #fbe3e4;"
            if minmatch:
                return "background: #e6efc2;"
    if index == 1:
        if maxmatch:
            return "background: #fbe3e4;"
        if minmatch:
            return "background: #e6efc2;"
    return ""


def table(results):
    sorted_tests = [
        'unix_benchmark_single',
        'unix_benchmark_multiple',
        'pgsql_mysql_benchmark',
        'django_pgsql_test',
        'django_sqlite3_test',
    ]
    output = []
    output.append("  <tr>")
    output.append("    <th>&nbsp;</th>")
    for i, test in enumerate(sorted_tests):
        output.append("    <th title=\"%s\">%s <span style=\"text-decoration:overline;\">x</span></th>" % (test, i+1))
        output.append("    <th title=\"%s\">%s &sigma;</th>" % (test, i+1))
    output.append("  </tr>")

    calculations = {}

    for host in HOSTS:
        hostkey, hostname = host
        calculations[hostkey] = {}
        for test in sorted_tests:
            scores_and_times = results[test][hostkey]
            scores = [s[0] for s in scores_and_times]
            avg = sum(scores, 0.0) / len(scores)
            std = numpy.std(scores)
            calculations[hostkey][test] = (avg, std)

    for host in HOSTS:
        hostkey, hostname = host
        output.append("  <tr>")
        output.append("    <td>%s</td>" % hostname)
        for test in sorted_tests:
            avg, std = calculations[hostkey][test]
            avg_style = style(0, avg, test, calculations)
            std_style = style(1, std, test, calculations)
            output.append("    <td style=\"text-align: right; %s\">%s</td>" % (avg_style, int(round(avg))))
            output.append("    <td style=\"text-align: right; %s\">%s</td>" % (std_style, round(std, 2)))
        output.append("  </tr>")

    print "\n".join(output)



if __name__ == "__main__":
    results = parse_benchmark_logs()
    #graph(results)
    table(results)
