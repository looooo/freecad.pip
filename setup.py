from setuptools import setup
from freecad.pipintegration.__version__ import __version__

setup(name='pip-integration',
      version=str(__version__),
      packages=['freecad',
                'freecad.pipintegration'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/looooo/pip-integration",
      description="pip installable addons for freecad",
      install_requires=[],
      include_package_data=True)
