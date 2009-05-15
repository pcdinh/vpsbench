import re

def parse(str):
    values = []
    p = re.compile("\s*([\w ,.]+):\s+\w+\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)")

    for line in [l for l in str.split("\n") if len(l)]:
        matches = p.search(line)
        city = matches.group(1)
        avg_ms = float(matches.group(3).replace(",", ""))
        values.append((city, avg_ms,))
    return values


prgmr = parse("""
 Florida, U.S.A.:       Okay    89.5    89.8    90.0
 Hong Kong, China:      Okay    228.3   228.5   228.8
 Sydney, Australia:     Okay    162.9   167.1   192.3
 New York, U.S.A.:      Okay    80.9    81.1    81.3
 Stockholm, Sweden:     Okay    175.6   178.2   182.5
 Santa Clara, U.S.A.:   Okay    5.3     5.6     5.9
 Vancouver, Canada:     Okay    23.3    23.6    24.7
 Krakow, Poland:        Okay    189.6   190.7   191.8
 London, United Kingdom:        Okay    149.6   150.1   150.4
 Madrid, Spain:         Okay    173.4   174.3   178.6
 Cagliari, Italy:       Okay    219.4   221.2   222.1
 Singapore, Singapore:  Okay    179.4   180.4   181.0
 Austin, U.S.A.:        Okay    201.1   201.3   201.5
 Cologne, Germany:      Okay    177.4   177.5   177.8
 Munchen, Germany:      Okay    180.1   180.5   180.9
 Amsterdam, Netherlands:        Okay    165.4   165.5   165.6
 Paris, France:         Okay    156.7   156.8   156.9
 Shanghai, China:       Okay    207.1   208.0   209.0
 Melbourne, Australia:  Okay    168.4   171.8   176.8
 Copenhagen, Denmark:   Okay    191.3   191.6   192.1
 Lille, France:         Okay    157.7   158.7   165.8
 San Francisco, U.S.A.:         Okay    2.6     2.8     3.0
 Chicago, U.S.A.:       Okay    55.3    55.9    57.4
 Zurich, Switzerland:   Okay    173.4   173.8   175.1
 Johannesburg, South Africa:    Okay    770.5   838.6   885.1
 Mumbai, India:         Okay    249.8   251.4   255.9
 Nagano, Japan:         Okay    116.7   117.1   117.4
 Haifa, Israel:         Okay    227.7   236.3   241.8
 Auckland, New Zealand:         Okay    245.2   247.5   248.8
 Groningen, Netherlands:        Okay    169.1   169.5   170.0
 Antwerp, Belgium:      Okay    163.7   164.2   164.6
 Dublin, Ireland:       Okay    158.3   158.7   159.0
 Moscow, Russia:        Okay    227.7   228.0   228.4
 Oslo, Norway:  Okay    200.1   200.4   201.1
""")

linode = parse("""
 Florida, U.S.A.:       Okay    33.0    34.0    37.2
 Hong Kong, China:      Okay    288.2   288.4   288.9
 Sydney, Australia:     Okay    236.8   237.6   238.9
 New York, U.S.A.:      Okay    10.3    10.7    11.5
 Stockholm, Sweden:     Okay    118.3   118.8   119.5
 Santa Clara, U.S.A.:   Okay    72.9    73.3    73.6
 Vancouver, Canada:     Okay    76.2    76.4    76.7
 Krakow, Poland:        Okay    108.8   109.5   110.8
 London, United Kingdom:        Okay    76.9    77.4    77.8
 Madrid, Spain:         Okay    94.7    95.4    95.8
 Cagliari, Italy:       Okay    131.5   134.7   136.6
 Singapore, Singapore:  Okay    265.4   266.4   267.3
 Austin, U.S.A.:        Okay    131.8   131.9   132.1
 Cologne, Germany:      Okay    97.9    98.0    98.2
 Munchen, Germany:      Okay    102.1   102.3   102.7
 Amsterdam, Netherlands:        Okay    85.5    85.7    85.9
 Paris, France:         Okay    84.4    84.6    84.8
 Shanghai, China:       Okay    275.2   276.4   278.0
 Melbourne, Australia:  Okay    242.0   243.3   245.8
 Copenhagen, Denmark:   Okay    92.6    92.8    93.0
 Lille, France:         Okay    91.5    93.7    102.6
 San Francisco, U.S.A.:         Okay    77.2    77.5    77.9
 Chicago, U.S.A.:       Okay    21.7    22.1    22.8
 Zurich, Switzerland:   Okay    100.3   101.6   103.6
 Johannesburg, South Africa:    Okay    1,071.6         1,157.3         1,200.6
 Mumbai, India:         Okay    197.3   198.5   201.2
 Nagano, Japan:         Okay    200.1   208.9   211.7
 Haifa, Israel:         Okay    154.8   156.5   158.2
 Auckland, New Zealand:         Okay    206.8   208.5   212.5
 Groningen, Netherlands:        Okay    95.3    95.7    96.2
 Antwerp, Belgium:      Okay    93.0    93.2    93.6
 Dublin, Ireland:       Okay    82.4    82.8    83.0
 Moscow, Russia:        Okay    152.6   152.8   153.1
 Oslo, Norway:  Okay    100.1   100.3   100.7

""")

slicehost = parse("""
 Florida, U.S.A.:       Okay    44.3    44.5    44.6
 Hong Kong, China:      Okay    211.8   212.1   213.0
 Sydney, Australia:     Okay    209.0   209.3   210.6
 New York, U.S.A.:      Okay    42.6    43.4    47.0
 Stockholm, Sweden:     Okay    140.8   140.9   141.0
 Santa Clara, U.S.A.:   Okay    47.2    48.4    55.0
 Vancouver, Canada:     Okay    50.8    51.1    51.3
 Krakow, Poland:        Okay    139.4   140.7   143.9
 London, United Kingdom:        Okay    96.3    97.1    97.8
 Madrid, Spain:         Okay    133.6   134.3   135.4
 Cagliari, Italy:       Okay    166.7   167.6   168.6
 Singapore, Singapore:  Okay    240.2   240.4   240.9
 Austin, U.S.A.:        Okay    36.3    36.5    36.7
 Cologne, Germany:      Okay    119.7   119.8   120.0
 Munchen, Germany:      Okay    122.1   122.4   122.8
 Amsterdam, Netherlands:        Okay    109.3   111.0   113.7
 Paris, France:         Okay    114.8   114.9   115.1
 Shanghai, China:       Okay    325.3   389.8   433.5
 Melbourne, Australia:  Okay    209.9   212.0   216.9
 Copenhagen, Denmark:   Okay    127.4   127.6   128.0
 Lille, France:         Okay    121.1   122.6   127.7
 San Francisco, U.S.A.:         Okay    45.6    45.9    46.1
 Chicago, U.S.A.:       Okay    6.2     6.6     6.9
 Zurich, Switzerland:   Okay    136.8   137.4   138.7
 Johannesburg, South Africa:    Okay    996.1   1,074.2         1,126.0
 Mumbai, India:         Okay    242.1   243.0   245.2
 Nagano, Japan:         Okay    184.3   189.4   200.6
 Haifa, Israel:         Okay    166.5   171.7   179.1
 Auckland, New Zealand:         Okay    179.2   179.7   180.3
 Groningen, Netherlands:        Okay    111.4   111.9   112.3
 Antwerp, Belgium:      Okay    109.4   109.6   109.9
 Dublin, Ireland:       Okay    107.7   108.2   108.7
 Moscow, Russia:        Okay    167.1   167.3   167.7
 Oslo, Norway:  Okay    145.7   145.9   146.4
""")
