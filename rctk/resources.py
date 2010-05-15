from rctk.resourceregistry import addResource, JSResource

addResource(JSResource('static/onion/onion.js'))
addResource(JSResource('static/onion/widget.js'))
addResource(JSResource('static/onion/core.js'))
addResource(JSResource('static/onion/util.js'))
addResource(JSResource('static/onion/jquery.js'))
addResource(JSResource('static/json2.js'))

import rctk.layouts.resources
import rctk.widgets.resources

