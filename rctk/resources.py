from rctk.resourceregistry import addResource, JSFileResource

addResource(JSFileResource('static/onion/onion.js'))
addResource(JSFileResource('static/onion/widget.js'))
addResource(JSFileResource('static/onion/core.js'))
addResource(JSFileResource('static/onion/util.js'))
addResource(JSFileResource('static/onion/jquery.js'))
addResource(JSFileResource('static/json2.js'))

import rctk.layouts.resources
import rctk.widgets.resources

