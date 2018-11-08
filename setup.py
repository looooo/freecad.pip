from setuptools import setup
import sys, os

version_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 
                            "freecad", "pip", "version.py")
with open(version_path) as fp:
    exec(fp.read())

setup(name='freecad.pip',
      version=__version__,
      packages=['freecad',
                'freecad.pip'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/looooo/pip-integration",
      description="pip installable addons for freecad",
      install_requires=[],
      include_package_data=True)
