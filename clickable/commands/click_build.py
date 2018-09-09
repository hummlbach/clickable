import os
import shutil

from .base import Command


class ClickBuildCommand(Command):
    aliases = ['build_click', 'build-click', 'click_build']
    name = 'click-build'
    help = 'Package the app into a click'

    def run(self, path_arg=None):
        command = 'click build {} --no-validate'.format(os.path.dirname(self.config.find_manifest()))

        self.container.run_command(command)

        if self.config.click_output:
            click = '{}_{}_{}.click'.format(self.config.find_package_name(), self.config.find_version(), self.config.arch)
            click_path = os.path.join(self.config.dir, click)
            output_file = os.path.join(self.config.click_output, click)

            if not os.path.exists(self.config.click_output):
                os.makedirs(self.config.click_output)

            print_info('Click outputted to {}'.format(output_file))
            shutil.copyfile(click_path, output_file)
