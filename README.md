# pip-integration (FreeCAD >= 0.17)

To support pip installable freecad-packages we need to have a tool which allows to graphically install this modules.


## Install:

`pip install https://github.com/looooo/pipintegration/archive/master.tar.gz`

## Console Usage:

```
from freecad.pipintegration import pip
pip.list()              # print a list of all installed packages
pip.install(pkg_name)   # installs the package with pkg_name (if in freecad_modules.json)
pip.uninstall(pkg_name) # uninstall the package.
```

## Gui

```
from freecad.pipintegration import widget
w = widget.PipWidget()
w.show()
```

![pip_gui_tool](docs/pip_gui_tool.png)

