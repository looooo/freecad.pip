import FreeCAD
import subprocess as subp
import threading
import json
import os
import copy

__dir__ = os.path.dirname(__file__)


def popenAndCall(onExit, *popenArgs):
    """
    Runs a subprocess.Popen, and then calls the function onExit when the
    subprocess completes.

    Use it exactly the way you'd normally use subprocess.Popen, except include a
    callable to execute as the first argument. onExit is a callable object, and
    *popenArgs and **popenKWArgs are simply passed up to subprocess.Popen.
    """
    def runInThread(onExit, popenArgs):
        proc = subp.Popen(*popenArgs, stdout=subp.PIPE, stderr=subp.PIPE)
        out, err = proc.communicate()
        onExit(out, err)
        return

    thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
    thread.start()
    return thread  # returns immediately after the thread starts


class _pip(object):
    def __init__(self):
        # we should get the file from github!
        # for testing it is included in this repo
        pkgs_file = os.path.join(__dir__, "freecad_modules.json")
        with open(pkgs_file, "r") as modules_file:
            data = json.load(modules_file)
        self.pkg_dict = {name: [source] for name, source in data.items()}
        self.update()

    def _command(self, command, call_back=None):
        '''
        trys to install the add_on with pip
        '''
        def message_call_back(out, err):
            if err:
                FreeCAD.Console.PrintMessage(out.decode("utf-8"))
                FreeCAD.Console.PrintError(err.decode("utf-8"))
            else:
                FreeCAD.Console.PrintMessage(out)
        call_back = call_back or message_call_back
        popenAndCall(call_back, command)
        return True

    def _check_pkg(self, pkg_name):
        if pkg_name in self.pkg_dict:
            return True

    def install(self, pkg_name, call_back=None):
        if self._check_pkg:
            FreeCAD.Console.PrintMessage(
                "pip install {}\n".format(self.pkg_dict[pkg_name][0]))
            self._command(["pip", "install", "-U",
                           self.pkg_dict[pkg_name][0], "--no-deps"],
                          call_back=call_back)

    def uninstall(self, pkg_name, call_back=None):
        if self._check_pkg:
            FreeCAD.Console.PrintMessage(
                "pip uninstall self.pkg_dict[pkg_name][0]]\n")
            self._command(["pip", "uninstall",
                           pkg_name, "-y"], call_back=call_back)

    def upgrade(self, pkg_name, call_back=None):
        if self._check_pkg:
            self._command(["pip", "install",
                           pkg_name, "--upgrade"], call_back=call_back)

    def list(self):
        pkgs = self.list_installed_pkgs()
        FreeCAD.Console.PrintMessage("INSTALLED PIP-PACKAGES:\n\n")
        for pkg in pkgs:
            FreeCAD.Console.PrintMessage(pkg + "\n")

    def update(self):
        self.installed_pkgs = self.list_installed_pkgs()
        temp_pkgs = copy.deepcopy(self.pkg_dict)
        for pkg, data in temp_pkgs.items():
            is_installed = pkg in self.installed_pkgs
            self.pkg_dict[pkg] = [data[0], is_installed]

    def list_installed_pkgs(self):
        installed_pkgs = []
        proc = subp.Popen(["pip", "list"], stdout=subp.PIPE, stderr=subp.PIPE)
        out, err = proc.communicate()
        out = out.decode("UTF-8")
        out = out.split("\n")
        for module in out:
            module = module.split(" ")[0]
            module_name = module.strip()
            if self._check_pkg(module_name):
                installed_pkgs.append(module_name)
        return installed_pkgs

    def check_dependencies(self, pkg_name):
        import importlib
        proc = subp.Popen(["pip", "show", pkg_name],
                          stdout=subp.PIPE, stderr=subp.PIPE)
        out, err = proc.communicate()
        if not out:
            FreeCAD.Console.PrintError(
                "no package {} found\n".format(pkg_name))
            return
        out = out.decode("UTF-8").split("\n")
        for line in out:
            if line.startswith("Requires:"):
                break
        else:
            return
        line = line.strip("Requires:")
        line = line.strip()
        # filter(None, ...) removes empty items
        deps = filter(None, line.split(", "))
        missing_deps = []

        for dep in deps:
            try:
                importlib.import_module(dep)
            except ImportError:
                missing_deps.append(dep)
                FreeCAD.Console.PrintWarning(
                    "Dependency {} is not installed\n".format(dep))
            else:
                FreeCAD.Console.PrintMessage(
                    "Dependency {} is installed\n".format(dep))
        return missing_deps


pip = _pip()
