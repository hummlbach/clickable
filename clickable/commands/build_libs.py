import os
import sys

from clickable.utils import (
    print_info,
    print_warning
)


from .base import Command
from clickable.utils import print_warning, get_builders, run_subprocess_check_call
from clickable.container import Container


class LibBuildCommand(Command):
    aliases = []
    name = 'build-libs'
    help = 'Compile the library dependencies'

    def run(self, path_arg=""):
        if not self.config.lib_configs:
            print_warning('No libraries defined.')

        single_lib = path_arg
        found = False

        for lib in self.config.lib_configs:
            if not single_lib or single_lib == lib.name:
                print_info("Building {}".format(lib.name))
                found = True

                lib.container_mode = self.config.container_mode
                lib.docker_image = self.config.docker_image
                lib.build_arch = self.config.build_arch
                lib.container = Container(lib, lib.name)
                lib.container.setup_dependencies()

                try:
                    os.makedirs(lib.build_dir)
                except FileExistsError:
                    pass
                except Exception:
                    print_warning('Failed to create the build directory: {}'.format(str(sys.exc_info()[0])))

                if lib.prebuild:
                    run_subprocess_check_call(lib.prebuild, cwd=self.config.cwd, shell=True)

                self.build(lib)

                if lib.postbuild:
                    run_subprocess_check_call(lib.postbuild, cwd=lib.build_dir, shell=True)

        if single_lib and not found:
            raise ValueError('Cannot build unknown library {}. You may add it to the clickable.json'.format(single_lib))

    def build(self, lib):
        builder_classes = get_builders()
        builder = builder_classes[lib.template](lib, None)
        builder.build()
