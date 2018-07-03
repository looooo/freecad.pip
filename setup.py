from setuptools import setup
import sys, os

sys.path.append(os.path.dirname(__file__))
from freecad.pipintegration import __version__
sys.path.pop(-1)

setup(name='pipintegration',
      version=__version__,
      packages=['freecad',
                'freecad.pipintegration'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/looooo/pip-integration",
      description="pip installable addons for freecad",
      install_requires=[],
      include_package_data=True)
