import getpass
import os.path


class OSState:
    VAGRANT_USERNAME = 'vagrant'
    VAGRANT_BASE_PATH = '/home/vagrant'

    def __init__(self):
        self._user = getpass.getuser()

    def is_vm(self):
        return self._user == self.VAGRANT_USERNAME

    @classmethod
    def get_vm_path(cls, path: str):
        return os.path.join(cls.VAGRANT_BASE_PATH, os.path.basename(path))

    def parse_path(self, path: str) -> str:
        return self.get_vm_path(path) if self.is_vm() else path
