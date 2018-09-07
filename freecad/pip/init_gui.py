import os
from PySide import QtCore, QtGui
import FreeCAD as App
import FreeCADGui as Gui


__dir__ = os.path.dirname(os.path.realpath(__file__))
icon = QtGui.QIcon(os.path.join(__dir__, "PipTool.svg"))

mw = Gui.getMainWindow()

from freecad.pip.gui import PipWidget
pip_widget = PipWidget(mw)
App._pip_widget = pip_widget

def onWorkbench():
    menu = mw.findChild(QtGui.QMenu, QtGui.QApplication.translate("menu", "&Tools"))
    action = QtGui.QAction(icon, "PipTools", menu)
    action.setIconVisibleInMenu(True)
    action.triggered.connect(startPip)
    menu.addAction(action)

def setup_menu_entry():
    if mw.property("eventLoop"):
        t.stop()
        onWorkbench()
        mw.workbenchActivated.connect(onWorkbench)

def startPip():
    App._pip_widget.show()

t = QtCore.QTimer()
t.timeout.connect(setup_menu_entry)
t.start(500)
