import pip
import pip._internal as pipintern
import json
import os
import copy
import tempfile

class _pip(object):
    def __init__(self):
        self.constraint_file = tempfile.mktemp(prefix="constraints", suffix=".txt")
        self.freeze()

    def _c_option(self):
        """
        internal fuction, returns the option to constraint packages
        """
        return "-c{}".format(self.constraint_file)

    def install(self, pkg_name):
        return pipintern.main(["install", pkg_name, "--user", self._c_option()])

    def uninstall(self, pkg_name):
        if pkg_name in [i[0] for i in self.list_user()]:
            return pipintern.main(["uninstall", pkg_name, "-y"])
        else:
            print("pkg is not a user-package")

    def _list(self):
        packages = pipintern.get_installed_distributions()
        user_packages = pipintern.get_installed_distributions(user_only=True)
        editable_packages = pipintern.get_installed_distributions(editables_only=True)
        system_packages = [pkg for pkg in packages if pkg not in user_packages + editable_packages]
        return packages, system_packages, user_packages, editable_packages
    
    @staticmethod
    def _convert_pkgs_list(pkg_list):
        output = []
        for pkg in pkg_list:
            output.append([pkg.project_name, pkg.version])
        return output
    
    def list(self):
        """
        lists all packages
        """
        packages = pipintern.get_installed_distributions()
        return self._convert_pkgs_list(packages)
    
    def list_user(self):
        packages = pipintern.get_installed_distributions(user_only=True)
        return self._convert_pkgs_list(packages)

    def list_editable(self):
        packages = pipintern.get_installed_distributions(editables_only=True)
        return self._convert_pkgs_list(packages)
    
    def list_system(self):
        return [pkg for pkg in self.list() if not pkg in self.list_editable() + self.list_user()]

    def update(self):
        """
        update all user packages
        """
        pass

    def freeze(self):
        """
        sets all installed packages fixed. This means these packages won't be updated.
        """
        with open(self.constraint_file, "w") as fp:
            for pkg_name, version in self.list_system():
                fp.write("{}=={}\n".format(pkg_name, version))         

    def set_fixed(self, pkg_name, fixed=True):
        """
        sets the package fixed, or release a fixed package if package is fixed and argument fixed is False
        """
        pass

    def select_user_install_dir(self, install_dir):
        """
        Advanced option to set the user install dir. This allows to use different directories
        for 3rd-party packages. This can be useful if different addons need different
        dependency-versions. This will require a restart of FreeCAD, because sys.path has to be 
        recomputed.
        """
        os.env["PYTHONUSERBASE"] = install_dir

pip = _pip()
