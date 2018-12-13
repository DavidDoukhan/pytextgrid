import re

def getintval(line, field_name):
    m = re.match(r'\s*%s\s*\=\s*(\d+)\s*'%field_name, line)
    return int(m.group(1))
	

def getfloatval(line, field_name):
    m = re.match(r'\s*%s\s*\=\s*((\w|\.)+)\s*'%field_name, line)
    f = float(m.group(1))
    return f


def getstringval(line, field_name):
    m = re.match(r'\s*%s\s*\=\s*\"(.*)\"\s*'%field_name, line)
    return m.group(1)
