import gi
gi.require_version('Gtk', '3.0')  # noqa: E402
gi.require_version('PangoCairo', '1.0')  # noqa: E402
# for some reason performance is improved by importing Gtk early
from gi.repository import Gtk as gtk

from hamster.lib import default_logger


logger = default_logger(__name__)

try:
    # defs.py is created by waf from defs.py.in
    from hamster import defs
    __version__ = defs.VERSION
    installed = True
except ImportError:
    # if defs is not there, we are running from sources
    from subprocess import getstatusoutput
    rc, output = getstatusoutput("git describe --tags --always --dirty=+")
    if rc == 0:
        # If available, prefer the git version, otherwise fall back to
        # the VERSION file (which is meaningful only in released
        # versions)
        __version__ = "{} (uninstalled)".format(output)
    else:
        from pathlib import Path
        with open(Path(__file__).parent / 'VERSION', 'r') as f:
            __version__ = f.read()
        del Path

    installed = False
    del getstatusoutput, rc, output

# cleanup namespace
del default_logger
del gtk  # performance is retained
