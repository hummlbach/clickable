import json
import shutil
import os

from .base import Builder
from clickable.config import Config


class GoBuilder(Builder):
    name = Config.GO

    def _ignore(self, path, contents):
        ignored = []
        for content in contents:
            cpath = os.path.abspath(os.path.join(path, content))
            if (
                cpath == os.path.abspath(self.config.install_dir) or
                cpath == os.path.abspath(self.config.build_dir) or
                content in self.config.ignore or
                content == 'clickable.json' or

                # Don't copy the go files, they will be compiled from the source directory
                os.path.splitext(content)[1] == '.go'
            ):
                ignored.append(content)

        return ignored

    def build(self):
        shutil.copytree(self.config.cwd, self.config.install_dir, ignore=self._ignore)

        gocommand = '/usr/local/go/bin/go build -pkgdir {}/.clickable/go -i -o {}/{} ..'.format(
            self.config.cwd,
            self.config.install_dir,
            self.config.find_app_name(),
        )
        self.config.container.run_command(gocommand)
