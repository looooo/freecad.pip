from PySide import QtGui, QtCore
import FreeCAD
from freecad.pip.app import pip


class PipWidget(QtGui.QTabWidget):
    def __init__(self, parent=None):
        super(PipWidget, self).__init__(parent=parent)
        self.addTab(PackageSystemWidget(self), "system")
        self.addTab(PackageUserWidget(self), "user")
        self.addTab(PackageDevelopWidget(self), "develop")

class PackageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PackageWidget, self).__init__(parent=parent)
        # list_widget with pip modules + install check
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
        self.dialog = InstallDialog(callback=self.update_pkg_list)
        self.dialog.show()

    def uninstall(self):
        self.dialog = UninstallDialog(self.current_item_name, callback=self.update_pkg_list)
        self.dialog.show()

class PackageDevelopWidget(PackageWidget):
    def __init__(self, parent):
        super(PackageDevelopWidget, self).__init__(parent)
        self.add_buttons()

    @property
    def packages(self):
        return pip.list_editable()

    def install(self):
        self.dialog = InstallDevelopDialog(callback=self.update_pkg_list)
        self.dialog.show()

    def uninstall(self):
        self.dialog = UninstallDialog(self.current_item_name, callback=self.update_pkg_list)
        self.dialog.show()


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

class InstallDialog(PipDialog):
    # TODO: must be file-path dialog!!!
    def __init__(self, parent=None, callback=None):
        super(InstallDialog, self).__init__(parent=parent, callback=callback)
        self.package_name.setPlaceholderText("enter name of package")

    def accept(self):
        pip.install(self.package_name.text())
        super(InstallDialog, self).accept()


class InstallDevelopDialog(PipDialog):
    def __init__(self, parent=None, callback=None):
        super(InstallDevelopDialog, self).__init__(parent=parent, callback=callback)
        self.package_name.setPlaceholderText("enter path to package")

    def accept(self):
        pip.install_develop(self.package_name.text())
        super(InstallDialog, self).accept()


class UninstallDialog(PipDialog):
    def __init__(self, package_name, parent=None, callback=None):
        super(UninstallDialog, self).__init__(parent=parent, callback=callback)
        self.package_name.setText(package_name)
        self.package_name.setEnabled(False)

    def accept(self):
        pip.uninstall(self.package_name.text())
        super(UninstallDialog, self).accept()
