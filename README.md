# pip-integration (FreeCAD >= 0.17)

To support pip installable freecad-packages we need to have a tool which allows to graphically install this modules.

## Install with pip directly:

`pip install https://github.com/looooo/freecad_pipintegration/archive/master.tar.gz`

## Install with pip from python command line (eg. from the FreeCAD-python-console)

```python
import subprocess as subp
import FreeCAD
url = "https://github.com/looooo/freecad_pipintegration/archive/master.tar.gz"
proc = subp.Popen(["pip", "install", url, "--user"], stdout=subp.PIPE, stderr=subp.PIPE)
out, err = proc.communicate()
FreeCAD.Console.PrintMessage(out.decode("utf8"))
FreeCAD.Console.PrintMessage(err.decode("utf8"))
```

# Usage 
## FreeCAD Console
Type the following in to the FreecAD console:
```python
from freecad.pip.app import pip
pip.list()                # print a list of all installed packages
```
This will ouput a list of packages you can install via pip.  
Use the following commands to install or uninstall said packages: 
```python
pip.install("pkg_name")   # installs the package with pkg_name (if in freecad_modules.json)
pip.uninstall("pkg_name") # uninstall the package.
```

## GUI (PipWidget)
Alternatively to the console (above solution) one can also utilize the GUI via what we call `PipWidget`. Enter the following in to the console and PipWidget will grant the ability to point and click on said pip packages (see screenshot). 
```
from freecad.pip.gui import PipWidget
widget = PipWidget()
widget.show()
```

![pip_gui_tool](docs/pip_gui_tool.png)

# Discussion
Further discussion of the FreeCAD forums: [pip-integration in Addon Manager](https://forum.freecadweb.org/viewtopic.php?f=22&t=29584)
