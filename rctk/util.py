def resolveclass(classid):
    m, k = classid.rsplit(".", 1)
    mod = __import__(m, fromlist=[k])
    klass = getattr(mod, k)
    return klass


