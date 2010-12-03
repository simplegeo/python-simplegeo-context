#!/usr/bin/env python
from setuptools import setup, find_packages
import os, re

PKG='simplegeo-context'
VERSIONFILE = os.path.join('simplegeo', 'context', '_version.py')
verstr = "unknown"
try:
    verstrline = open(VERSIONFILE, "rt").read()
except EnvironmentError:
    pass # Okay, there is no version file.
else:
    VSRE = r"^verstr = ['\"]([^'\"]*)['\"]"
    mo = re.search(VSRE, verstrline, re.M)
    if mo:
        verstr = mo.group(1)
    else:
        print "unable to find version in %s" % (VERSIONFILE,)
        raise RuntimeError("if %s.py exists, it must be well-formed" % (VERSIONFILE,))

setup_requires = []
tests_require = ['mock']

# nosetests is an optional way to get code-coverage results. Uncomment
# the following and run "python setup.py nosetests --with-coverage.
# --cover-erase --cover-tests --cover-inclusive --cover-html"
# tests_require.extend(['coverage', 'nose'])

# trialcoverage is another optional way to get code-coverage
# results. Uncomment the following and run "python setup.py trial
# --reporter=bwverbose-coverage -s simplegeo.context.test".
# setup_requires.append('setuptools_trial')
# tests_require.extend(['setuptools_trial', 'trialcoverage'])

# As of 2010-11-22 neither of the above options appear to work to
# generate code coverage results, but the following does:
# rm -rf ./.coverage* htmlcov ; coverage run --branch  --include=simplegeo/* setup.py test -s simplegeo.context.test && coverage html

setup(name=PKG,
      version=verstr,
      description="Library for interfacing with SimpleGeo's Context API",
      author="Zooko Wilcox-O'Hearn",
      author_email="zooko@simplegeo.com",
      url="http://github.com/simplegeo/python-simplegeo-context",
      packages = find_packages(),
      license = "MIT License",
      # install_requires=['simplegeo-shared >= 1.9'], # We have a problem with namespace packages in Debian, and commenting-out this let's the debian install of python-simplegeo-context use the debian install of python-simplegeo-shared even though pkg_resources can't tell that the debian install of python-simplegeo-shared has provided the "simplegeo-shared" Python package.
      install_requires=[],
      keywords="simplegeo",
      zip_safe=False, # actually it is zip safe, but zipping packages doesn't help with anything and can cause some problems (http://bugs.python.org/setuptools/issue33 )
      namespace_packages = ['simplegeo'],
      setup_requires=setup_requires,
      tests_require=tests_require)
