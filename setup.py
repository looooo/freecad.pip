from setuptools import setup
from freecad.pipintegration import __version__

setup(name='pipintegration',
      version=str(__version__),
      packages=['freecad',
                'freecad.pipintegration'],
      maintainer="looooo",
      maintainer_email="sppedflyer@gmail.com",
      url="https://github.com/looooo/pip-integration",
      description="pip installable addons for freecad",
      install_requires=[],
      include_package_data=True)
