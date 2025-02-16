import os
import shlex
import subprocess
from pathlib import Path

from clickable.utils import (
    check_command,
    print_warning,
    print_info
)
from .base import Command
from .build import BuildCommand
from .clean import CleanCommand
from .docker.debug_gdb_support import DebugGdbSupport
from .docker.docker_config import DockerConfig
from .docker.go_support import GoSupport
from .docker.nvidia_support import NvidiaSupport
from .docker.rust_support import RustSupport
from .docker.webapp_support import WebappSupport


class DesktopCommand(Command):
    aliases = []
    name = 'desktop'
    help = 'Run the app on your desktop'

    def run(self, path_arg=None):
        self.prepare_run(self.config)
        docker_config = self.setup_docker(self.config)
        self.run_docker_command(docker_config, verbose_mode=self.config.debug)

    def prepare_run(self, config):
        self.validate_lxd_for_desktop_mode(config.lxd)
        self.run_clean_and_build_commands(config)

    def validate_lxd_for_desktop_mode(self, is_lxd_requested):
        if is_lxd_requested:
            raise Exception('Using lxd for desktop mode is not supported')

    def run_clean_and_build_commands(self, config):
        if not config.dirty:
            CleanCommand(config).run()
        BuildCommand(config).run()

    def setup_docker(self, config):
        self.ensure_docker_daemon_is_setup_and_running(config)
        self.allow_docker_to_connect_to_xserver()
        docker_config = self.setup_docker_config(config)
        return docker_config

    def ensure_docker_daemon_is_setup_and_running(self, config):
        config.container.check_docker()

    def allow_docker_to_connect_to_xserver(self):
        if self.is_xhost_installed():
            subprocess.check_call(shlex.split('xhost +local:docker'))
        else:
            print_warning('xhost not installed, desktop mode may fail')

    def is_xhost_installed(self):
        try:
            check_command('xhost')
            return True
        except Exception:  # TODO catch a specific Exception
            return False

    def setup_docker_config(self, config):
        docker_config = DockerConfig()

        docker_config.uid = os.getuid()
        docker_config.docker_image = config.container.docker_image
        docker_config.working_directory = config.install_dir
        docker_config.use_nvidia = config.use_nvidia

        docker_config.execute = self.determine_executable(
            self.determine_path_of_desktop_file(config)
        )

        package_name = config.find_package_name()

        docker_config.add_volume_mappings(
            self.setup_volume_mappings(
                config.cwd,
                package_name
            )
        )

        docker_config.add_environment_variables(
            self.setup_environment(docker_config.working_directory)
        )

        NvidiaSupport().update(docker_config)

        WebappSupport(package_name).update(docker_config)

        GoSupport(config).update(docker_config)

        RustSupport(config).update(docker_config)

        DebugGdbSupport(config).update(docker_config)

        return docker_config

    def determine_path_of_desktop_file(self, config):
        desktop_path = None
        hooks = config.get_manifest().get('hooks', {})
        app = config.find_app_name()
        if app:
            if app in hooks and 'desktop' in hooks[app]:
                desktop_path = hooks[app]['desktop']
        else:
            # TODO config.find_app_name never returns None. It raises an exception
            for key, value in hooks.items():
                if 'desktop' in value:
                    desktop_path = value['desktop']
                    break

        if not desktop_path:
            raise Exception('Could not find desktop file for app "{}"'.format(app))

        # TODO finding the configured desktop entry should be moved to Config
        # We could then proceed here with making it an absolute path and
        # checking if it exists
        desktop_path = os.path.join(config.install_dir, desktop_path)
        if not os.path.exists(desktop_path):
            raise Exception('Could not determine executable. Desktop file does not exist: "{}"'.format(desktop_path))

        return desktop_path

    def determine_executable(self, desktop_path):
        execute = self.find_configured_exec_in_desktop_file(desktop_path)
        if not execute:
            raise Exception('No "Exec" line found in the desktop file {}'.format(desktop_path))

        return execute.replace('Exec=', '').strip()

    def find_configured_exec_in_desktop_file(self, desktop_path):
        with open(desktop_path, 'r') as desktop_file:
            for line in desktop_file.readlines():
                if line.startswith('Exec='):
                    return line

        return None

    def setup_environment(self, working_directory):
        lib_path = self.get_docker_lib_path_env(working_directory)

        return {
            'XAUTHORITY': '/tmp/.docker.xauth',
            'DISPLAY': os.environ['DISPLAY'],
            'QML2_IMPORT_PATH': lib_path,
            'LD_LIBRARY_PATH': lib_path,
            'PATH': self.get_docker_path_env(working_directory),
            'HOME': '/home/phablet',
            'OXIDE_NO_SANDBOX': '1',
        }

    def get_docker_lib_path_env(self, working_directory):
        return ':'.join([
            os.path.join(working_directory, 'lib/x86_64-linux-gnu'),
            os.path.join(working_directory, 'lib'),
            '/usr/local/nvidia/lib',
            '/usr/local/nvidia/lib64',
        ])

    def get_docker_path_env(self, working_directory):
        return ':'.join([
            '/usr/local/nvidia/bin',
            '/bin',
            '/usr/bin',
            os.path.join(working_directory, 'bin'),
            os.path.join(working_directory, 'lib/x86_64-linux-gnu/bin'),
            working_directory,
        ])

    def setup_volume_mappings(self, local_working_directory, package_name):
        xauth_path = self.touch_xauth()

        share_path = self.makedirs('/tmp/clickable/share/{package}/{package}'.format(package=package_name))
        cache_path = self.makedirs('/tmp/clickable/cache/{package}/{package}'.format(package=package_name))
        config_path = self.makedirs('/tmp/clickable/config/{package}/{package}'.format(package=package_name))

        return {
            local_working_directory: local_working_directory,
            '/tmp/.X11-unix': '/tmp/.X11-unix',
            xauth_path: xauth_path,
            share_path: '/home/phablet/.local/share',
            cache_path: '/home/phablet/.cache',
            config_path: '/home/phablet/.config'
        }

    def touch_xauth(self):
        xauth_path = '/tmp/.docker.xauth'
        Path(xauth_path).touch()
        return xauth_path

    def makedirs(self, path):
        os.makedirs(path, 0o777, True)
        return path

    def run_docker_command(self, docker_config, verbose_mode):
        command = docker_config.render_command()
        if verbose_mode:
            print_info(command)

        subprocess.check_call(shlex.split(command), cwd=docker_config.working_directory)
