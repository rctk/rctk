from rctk.resourceregistry import addResource, JSFileResource, CSSFileResource

addResource(JSFileResource('resources/base.js'))
addResource(JSFileResource('resources/root.js'))
addResource(JSFileResource('resources/button.js'))
addResource(JSFileResource('resources/checkbox.js'))
addResource(JSFileResource('resources/dropdown.js'))
addResource(JSFileResource('resources/frame.js'))
addResource(JSFileResource('resources/list.js'))
addResource(JSFileResource('resources/panel.js'))
addResource(JSFileResource('resources/statictext.js'))
addResource(JSFileResource('resources/text.js'))
addResource(JSFileResource('resources/statictext.js'))
addResource(JSFileResource('resources/password.js'))
addResource(JSFileResource('resources/datetext.js'))

addResource(JSFileResource('resources/jgrid/js/jquery.jqGrid.min.js'))
addResource(CSSFileResource('resources/jgrid/css/ui.jqgrid.css'))

addResource(JSFileResource('resources/grid.js'))
addResource(JSFileResource('resources/image.js'))
addResource(JSFileResource('resources/collection.js'))

## jScrollPane support
addResource(JSFileResource("resources/jScrollPane/jScrollPane.js"))
addResource(JSFileResource("resources/jScrollPane/jquery.mousewheel.js"))
addResource(CSSFileResource("resources/jScrollPane/jScrollPane.css"))
