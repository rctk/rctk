import types

def resolveclass(classid):
    ## if it's not a string, assume it won't need resolving
    if not isinstance(classid, types.StringTypes):
        return classid

    m, k = classid.rsplit(".", 1)
    mod = __import__(m, globals(), locals(), [k])
    klass = getattr(mod, k)
    return klass

def un_unicode(d):
    """ transform unicode keys to normal """
    return dict((str(k), v) for (k,v) in d.items())

