def resolveclass(classid):
    m, k = classid.rsplit(".", 1)
    mod = __import__(m, fromlist=[k])
    klass = getattr(mod, k)
    return klass

def un_unicode(d):
    """ transform unicode keys to normal """
    return dict((str(k), v) for (k,v) in d.items())

