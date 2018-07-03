from PySide import QtGui, QtCore
import FreeCAD
from freecad.pip.app import pip


class PipWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PipWidget, self).__init__(parent=parent)
        # list_widget with pip modules + install check
        self.setLayout(QtGui.QVBoxLayout())
        self.pip = pip
        self.Qpip_list = QtGui.QListWidget(self)
        self.Qpip_list.setIconSize(QtCore.QSize(16, 16))
        self.layout().addWidget(self.Qpip_list)
        self.update_pkg_list()

        self.install_button = QtGui.QPushButton("install")
        self.check_deps_button = QtGui.QPushButton("check dependencies")
        self.uninstall_button = QtGui.QPushButton("uninstall")
        self.button_widget = QtGui.QWidget(self)
        self.button_widget.setLayout(QtGui.QHBoxLayout())
        self.button_widget.layout().addWidget(self.install_button)
        self.button_widget.layout().addWidget(self.check_deps_button)
        self.button_widget.layout().addWidget(self.uninstall_button)
        self.layout().addWidget(self.button_widget)

        self.install_button.clicked.connect(self.install)
        self.uninstall_button.clicked.connect(self.uninstall)
        self.check_deps_button.clicked.connect(self.check_dependencies)
        self.Qpip_list.currentItemChanged.connect(self.item_changed)

    def current_pkg_name(self):
        return self.Qpip_list.currentItem().text()

    def current_pkg_item(self):
        return self.pip.pkg_dict[self.current_pkg_name()]

    def install(self, *args):
        self.pip.install(self.current_pkg_name(), call_back=self.end_command)

    def uninstall(self, *args):
        self.pip.uninstall(self.current_pkg_name(), call_back=self.end_command)

    def check_dependencies(self, *args):
        missing_deps = self.pip.check_dependencies(self.current_pkg_name())
        if missing_deps:
            # show dialog with names of missing deps
            pass

    def end_command(self, out, err):
        if err:
            FreeCAD.Console.PrintMessage(out.decode("utf-8"))
            FreeCAD.Console.PrintError(err.decode("utf-8"))
        else:
            FreeCAD.Console.PrintMessage(out.decode("utf-8"))
        self.update_pkg_list()

    def update_pkg_list(self):
        self.Qpip_list.clear()
        icon = QtGui.QIcon.fromTheme("dialog-ok")
        self.pip.update()
        for name, [url, is_installed] in self.pip.pkg_dict.items():
            if is_installed:
                self.Qpip_list.addItem(QtGui.QListWidgetItem(icon, name))
            else:
                self.Qpip_list.addItem(QtGui.QListWidgetItem(name))

    def item_changed(self):
        if self.Qpip_list.currentItem():  # can be none too
            pkg, installed = self.current_pkg_item()
            if installed:
                self.install_button.setEnabled(False)
                self.uninstall_button.setEnabled(True)
                self.check_deps_button.setEnabled(True)
            else:
                self.install_button.setEnabled(True)
                self.uninstall_button.setEnabled(False)
                self.check_deps_button.setEnabled(True)
