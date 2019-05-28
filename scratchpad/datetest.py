import datetime
from _datetime import timedelta
fmt = '%Y-%m-%d_%H:%M:%S %Z'
fmt2 = '%Y-%m-%d_%H:%M'
fmtical = '%Y%m%dT%H%M00Z'
d = datetime.datetime.now(datetime.timezone(timedelta()))
d_string = d.strftime(fmt)
d2 = datetime.datetime.strptime(d_string, fmt)
print(d_string)
print(d2.strftime(fmt))
d3 = datetime.datetime.strptime("2017-09-01_19:30:00 UTC", fmt)
print(d3)
print(d3.strftime(fmt))
d4 = datetime.datetime.strptime("2017-09-01_19:30", fmt2)
print(d4.strftime(fmtical))

d5 = d4 + timedelta(hours=+3)
print(d5.strftime(fmtical))
