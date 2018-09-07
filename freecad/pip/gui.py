from PySide import QtGui, QtCore
import FreeCAD
from freecad.pip.app import pip


class PipWidget(QtGui.QDialog):
    def __init__(self, parent=None):
        super(PipWidget, self).__init__(parent=parent)
        self.setLayout(QtGui.QHBoxLayout())
        self.tab_widget = QtGui.QTabWidget(self)
        self.layout().addWidget(self.tab_widget)
        self.tab_widget.addTab(PackageSystemWidget(self), "system")
        self.tab_widget.addTab(PackageUserWidget(self), "user")
        self.tab_widget.addTab(PackageDevelopWidget(self), "develop")

class PackageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PackageWidget, self).__init__(parent=parent)
        self.setLayout(QtGui.QVBoxLayout())
        self.Qpip_list = QtGui.QListWidget(self)
        self.layout().addWidget(self.Qpip_list)
        self.update_pkg_list()

    def add_buttons(self):
        self.button_widget = QtGui.QWidget(self)
        self.install_button = QtGui.QPushButton("install")
        self.uninstall_button = QtGui.QPushButton("uninstall")
        self.button_widget.setLayout(QtGui.QHBoxLayout())
        self.button_widget.layout().addWidget(self.install_button)
        self.button_widget.layout().addWidget(self.uninstall_button)
        self.layout().addWidget(self.button_widget)

        self.install_button.clicked.connect(self.install)
        self.uninstall_button.clicked.connect(self.uninstall)
        self.Qpip_list.currentItemChanged.connect(self.item_changed)
        self.item_changed()

    @property
    def current_item_name(self):
        return self.Qpip_list.currentItem().text()

    def update_pkg_list(self):
        """
        packages = [[name, version], [n, v], ...]
        """
        self.Qpip_list.clear()
        for n, v in self.packages:
            self.Qpip_list.addItem(QtGui.QListWidgetItem(n))

    def item_changed(self):
        if self.Qpip_list.currentItem():
            self.uninstall_button.setEnabled(True)
        else:
            self.uninstall_button.setEnabled(False)

class PackageSystemWidget(PackageWidget):
    @property
    def packages(self):
        return pip.list_system()

class PackageUserWidget(PackageWidget):
    def __init__(self, parent):
        super(PackageUserWidget, self).__init__(parent)
        self.add_buttons()

    @property
    def packages(self):
        return pip.list_user()

    def install(self):
        name, ok = QtGui.QInputDialog.getText(self,
            "install package", "package name")
        if ok and name:
            pip.install(name)
            self.update_pkg_list()

    def uninstall(self):
        ok_button = QtGui.QMessageBox.Ok
        button_pressed = QtGui.QMessageBox.question(
            self,
            "uninstall user package",
            "Uninstalling package '{}'?".format(self.current_item_name),
            QtGui.QMessageBox.Cancel|ok_button
            )
        if button_pressed == ok_button:
            pip.uninstall(self.current_item_name)
            self.update_pkg_list()


class PackageDevelopWidget(PackageWidget):
    def __init__(self, parent):
        super(PackageDevelopWidget, self).__init__(parent)
        self.add_buttons()

    @property
    def packages(self):
        return pip.list_editable()

    def install(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, "select package directory", QtCore.QDir.currentPath())
        if path:
            pip.install_develop(path)
            self.update_pkg_list()

    def uninstall(self):
        ok_button = QtGui.QMessageBox.Ok
        button_pressed = QtGui.QMessageBox.question(
            self,
            "uninstall development package",
            "Uninstalling package '{}'?".format(self.current_item_name),
            QtGui.QMessageBox.Cancel|ok_button
            )
        if button_pressed == ok_button:
            pip.uninstall(self.current_item_name)
            self.update_pkg_list()


class PipDialog(QtGui.QDialog):
    def __init__(self, parent=None, callback=None):
        super(PipDialog, self).__init__(parent=parent)
        self.package_name = QtGui.QLineEdit()
        self.setLayout(QtGui.QVBoxLayout())
        self.layout().addWidget(self.package_name)
        self.accept_button = QtGui.QPushButton("Ok")
        self.reject_button = QtGui.QPushButton("Cancel")
        self.button_widget = QtGui.QWidget()
        self.button_widget.setLayout(QtGui.QHBoxLayout())
        self.button_widget.layout().addWidget(self.accept_button)
        self.button_widget.layout().addWidget(self.reject_button)
        self.accept_button.clicked.connect(self.accept)
        self.reject_button.clicked.connect(self.reject)
        self.layout().addWidget(self.button_widget)
        self.callback = callback

    def accept(self):
        self.callback()
        super(PipDialog, self).accept()
