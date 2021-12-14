"""Used for determining whether system is running inside of vagrant or not."""
from __future__ import annotations
import getpass
import os.path


class OSState:
    """Class to determine whether system is running inside of vagrant or not.

    Class looks at the username of the current OS. Will have username `vagrant` if
    system is running inside of Vagrant.
    """

    VAGRANT_USERNAME = "vagrant"
    VAGRANT_BASE_PATH = "/home/vagrant"

    def __init__(self) -> None:
        """Get username from system."""
        self._user = getpass.getuser()

    def is_vm(self) -> bool:
        """Returns whether OS is inside a vm."""
        return self._user == self.VAGRANT_USERNAME

    @classmethod
    def get_vm_path(cls, path: str) -> str:
        """Returns path modified to be a vm path."""
        return os.path.join(cls.VAGRANT_BASE_PATH, os.path.basename(path))

    def parse_path(self, path: str) -> str:
        """If running in vm return vm path. If not, return passed path."""
        return self.get_vm_path(path) if self.is_vm() else path
