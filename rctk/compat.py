import sys

if sys.version_info[0] == 3:    
    ## python 3
    import json
    from collections import OrderedDict
    from urllib.parse import parse_qs
    python3 = True
else:
    import simplejson as json
    ## actually not necessary under 2.7!
    from rctk.odict import OrderedDict
    from cgi import parse_qs
    python3 = False
