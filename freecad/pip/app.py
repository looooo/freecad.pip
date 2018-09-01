import os
import platform
import copy
import tempfile
import subprocess as subp
import FreeCAD

print_msg = FreeCAD.Console.PrintMessage
print_err = FreeCAD.Console.PrintError

def process(*args, silent=True):
    if not silent:
        command = ""
        for i in args:
            command += i + " "
        print_msg(command)
        print_msg("\n")
    shell = False
    if platform.system == "Windows":
        shell = True
    proc = subp.Popen(args, shell=shell, stdout=subp.PIPE, stderr=subp.PIPE)
    out, err = proc.communicate()
    if err:
        raise RuntimeError(err.decode("utf8"))
    return out.decode("utf8")

class _pip(object):
    def __init__(self):
        self.constraint_file = tempfile.mktemp(prefix="constraints", suffix=".txt")
        self.freeze()

    def _c_option(self):
        """
        internal fuction, returns the option to constraint packages
        """
        return "-c{}".format(self.constraint_file)

    @staticmethod
    def _convert_pkgs_list(text):
        if text:
            return [i.split()[:2] for i in text.split("\n")[2:-1]]
        else:
            return []

    def install(self, pkg_name):
        print_msg(process("pip", "install", pkg_name, "--user", self._c_option(), silent=False))
    
    def install_develop(self, fp):
        print_msg(process("pip", "install", "-e", fp, "--user", self._c_option(), silent=False))

    def uninstall(self, pkg_name):
        assert(pkg_name in [i[0] for i in self.list_user() + self.list_editable()])
        print_msg(process("pip", "uninstall", pkg_name, "-y", silent=False))
        print_msg("\n")
    
    def list(self):
        """
        lists all packages
        """
        packages = process("pip", "list")
        return self._convert_pkgs_list(packages)
    
    def list_user(self):
        """
        lists all user packages
        """
        packages = process("pip", "list", "--user")
        return self._convert_pkgs_list(packages)

    def list_editable(self):
        """
        lists all packages
        """
        packages = process("pip", "list", "--editable")
        return self._convert_pkgs_list(packages)
    
    def list_system(self):
        editable = self.list_editable()
        user = self.list_user()
        non_system = editable + user
        return [pkg for pkg in self.list() if not pkg in non_system]

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
        Advanced option to sets the user install dir. This allows to use different directories
        for 3rd-party packages. This can be useful if different addons need different
        dependency-versions. This will require a restart of FreeCAD, because sys.path has to be 
        recomputed.
        """
        os.env["PYTHONUSERBASE"] = install_dir

pip = _pip()

