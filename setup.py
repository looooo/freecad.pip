from setuptools import setup
import sys, os

sys.path.append(os.path.dirname(__file__))
from freecad.pip import __version__
sys.path.pop(-1)

setup(name='freecad_pip',
      version=__version__,
      packages=['freecad',
                'freecad.pip'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/looooo/pip-integration",
      description="pip installable addons for freecad",
      install_requires=[],
      include_package_data=True)
