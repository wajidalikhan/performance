def modify_printed_string(type,string):
    return "%s%s\033[0m"%(type,string)

def red(string):
    return modify_printed_string('\x1b[0;31m',string)

def green(string):
    return modify_printed_string('\x1b[0;32m',string)

def yellow(string):
    return modify_printed_string('\x1b[0;33m',string)

def blue(string):
    return modify_printed_string('\x1b[0;34m',string)

def magenta(string):
    return modify_printed_string('\x1b[0;35m',string)

def cyan(string):
    return modify_printed_string('\x1b[0;36m',string)

def bold(string):
    return modify_printed_string('\033[1m',string)

def prettydict(d, indent=4, color=blue):
    space = max([0]+[len(str(x)) for x in d])+2
    print('')
    for key, value in d.items():
        print(color(" "*indent + str(key)),end='')
        if isinstance(value, dict):
            prettydict(value, indent=len(" "*(space)), color=color)
        else:
            print(color(" "*(space-len(key)) + str(value)))
