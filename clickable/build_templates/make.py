import subprocess
import shutil
import sys
import os

from .base import Builder
from clickable.utils import print_warning
from clickable.config import Config


class MakeBuilder(Builder):
    def post_make(self):
        if self.config.postmake:
            subprocess.check_call(self.config.postmake, cwd=self.config.build_dir, shell=True)

    def make(self):
        command = 'make'
        if self.config.make_args:
            command = '{} {}'.format(command, ' '.join(self.config.make_args))

        self.config.container.run_command(command)

    def make_install(self):
        if os.path.exists(self.config.install_dir) and os.path.isdir(self.config.install_dir):
            shutil.rmtree(self.config.install_dir)

        try:
            os.makedirs(self.config.install_dir)
        except FileExistsError:
            print_warning('Failed to create temp dir, already exists')
        except Exception:
            print_warning('Failed to create temp dir ({}): {}'.format(self.config.install_dir, str(sys.exc_info()[0])))

        # The actual make command is implemented in the subclasses

    def build(self):
        self.make()
        self.post_make()
        self.make_install()
