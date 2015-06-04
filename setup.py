#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
import os
from os.path import exists, isdir, join
import platform
import re
import shutil
import sys

if sys.platform=='win32':
    assert platform.architecture()[0]=='32bit', 'Assumes a Python built for 32bit'
    import py2exe
    dist_dir = 'dist.win32'
elif sys.platform=='darwin':
    dist_dir = 'dist.macosx'
else:
    assert False, 'Unsupported platform %s' % sys.platform

if dist_dir and len(dist_dir)>1 and isdir(dist_dir):
    shutil.rmtree(dist_dir)

# "Developer ID Application" name for signing
macdeveloperid = None


# Patch py2app recipe enumerator to skip the sip recipe since it's too enthusiastic - we'll list additional Qt modules explicitly
if sys.platform=='darwin':
    from py2app import recipes
    import py2app.build_app
    def iterRecipes(module=recipes):
        for name in dir(module):
            if name.startswith('_') or name=='sip':
                continue
            check = getattr(getattr(module, name), 'check', None)
            if check is not None:
                yield (name, check)
    py2app.build_app.iterRecipes = iterRecipes


APP = 'EDMarketConnector.py'
APPNAME = re.search(r"^appname\s*=\s*'(.+)'", file('config.py').read(), re.MULTILINE).group(1)
APPLONGNAME = re.search(r"^applongname\s*=\s*'(.+)'", file('config.py').read(), re.MULTILINE).group(1)
VERSION = re.search(r"^appversion\s*=\s*'(.+)'", file('config.py').read(), re.MULTILINE).group(1)
SHORTVERSION = ''.join(VERSION.split('.')[:3])

PY2APP_OPTIONS = {'dist_dir': dist_dir,
                  'optimize': 2,
                  'packages': [ 'requests' ],
                  'excludes': [ 'PIL' ],
                  'iconfile': '%s.icns' % APPNAME,
                  'semi_standalone': True,
                  'site_packages': False,
                  'plist': {
                      'CFBundleName': APPNAME,
                      'CFBundleIdentifier': 'uk.org.marginal.%s' % APPNAME.lower(),
                      'CFBundleShortVersionString': VERSION,
                      'CFBundleVersion':  VERSION,
                      'LSMinimumSystemVersion': '.'.join(platform.mac_ver()[0].split('.')[:2]),	# minimum version = build version
                      'NSHumanReadableCopyright': u'© 2015 Jonathan Harris',
                  },
                  'graph': True,	# output dependency graph in dist
              }

PY2EXE_OPTIONS = {'dist_dir': dist_dir,
                  'optimize': 2,
                  'packages': [ 'requests' ],
                  'excludes': [ 'PIL' ],
              }

if sys.platform=='win32':
    import requests
    DATA_FILES = [ ('', [requests.certs.where(),
                         '%s.ico' % APPNAME ] ) ]
else:
    DATA_FILES = [ ]

setup(
    name = APPLONGNAME,
    version = VERSION,
    app = [APP],
    windows = [ {'script': APP,
                 'icon_resources': [(0, '%s.ico' % APPNAME)],
                 'copyright': u'© 2015 Jonathan Harris',
             } ],
    data_files = DATA_FILES,
    options = { 'py2app': PY2APP_OPTIONS,
                'py2exe': PY2EXE_OPTIONS },
    setup_requires = [sys.platform=='darwin' and 'py2app' or 'py2exe'],
)


if sys.platform == 'darwin':
    if isdir('%s/%s.app' % (dist_dir, APPNAME)):
        if macdeveloperid:
            os.system('codesign --deep -v -s "Developer ID Application: %s" %s/%s.app' % (macdeveloperid, dist_dir, APPNAME))
        # Make zip for distribution, preserving signature
        os.system('cd %s; ditto -ck --keepParent --sequesterRsrc %s.app ../%s_mac_%s.zip; cd ..' % (dist_dir, APPNAME, APPNAME, SHORTVERSION))
else:
    # Manually trim the tcl/tk folders
    os.unlink(join(dist_dir, 'w9xpopen.exe'))
    for d in [ r'tcl\tcl8.5\encoding',
               r'tcl\tcl8.5\http1.0',
               r'tcl\tcl8.5\msgs',
               r'tcl\tcl8.5\tzdata',
               r'tcl\tk8.5\demos',
               r'tcl\tk8.5\images',
               r'tcl\tk8.5\msgs', ]:
        shutil.rmtree(join(dist_dir, d))
    os.system(r'"C:\Program Files (x86)\WiX Toolset v3.9\bin\candle.exe" -out %s\ %s.wxs' % (dist_dir, APPNAME))
    if exists('%s/%s.wixobj' % (dist_dir, APPNAME)):
        os.system(r'"C:\Program Files (x86)\WiX Toolset v3.9\bin\light.exe" -sacl -spdb %s\%s.wixobj -out %s_win_%s.msi' % (dist_dir, APPNAME, APPNAME, SHORTVERSION))
