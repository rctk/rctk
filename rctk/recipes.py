from zc.recipe import egg
import zc.buildout


class WSGI(object):
    """ provide a buildout wsgi entrypoint"""

    template = """%(relative_paths_setup)s
import sys
sys.path[0:0] = [
  %(path)s,
  ]

from rctk.wsgi import application
"""
    def __init__(self, buildout, name, options):
        self.buildout, self.name, self.options = buildout, name, options

        python = options.get('python', buildout['buildout']['python'])
        options['executable'] = buildout[python]['executable']
        options['bin-directory'] = buildout['buildout']['bin-directory']
        options.setdefault('eggs', 'zc.recipe.egg')

        self.zcegg = egg.Egg(buildout, options['recipe'], options)

    def install(self):
        """installer"""

        options = self.options
        reqs, ws = self.zcegg.working_set([options['recipe']])

        _script_template = zc.buildout.easy_install.script_template
        zc.buildout.easy_install.script_template = zc.buildout.easy_install.script_header + self.template
        scripts = zc.buildout.easy_install.scripts(
            [(self.name, options['recipe']+'.ctl', 'run')],
            ws,
            options['executable'],
            options['bin-directory'],
            arguments = [],
            )

        zc.buildout.easy_install.script_template = _script_template
        return scripts

    def update(self):
        """updater"""
        self.install()
