import py.cmdline
import sys
def runall():
    args = sys.argv[1:]
    args += ["-k", "rctk"]
    py.cmdline.pytest(args)

