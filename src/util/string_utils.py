def mk_int(s):
    s = s.strip()
    return int(s) if s else 0


def mk_float(s):
    s = s.strip()
    return float(s) if s else 0.0


def mk_str_2(f):
    return '{0:.2f}'.format(f)


def mk_str_4(f):
    return '{0:.4f}'.format(f)


def mk_str_int(f):
    return '{0:.0f}'.format(f)