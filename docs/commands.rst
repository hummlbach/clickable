.. _commands:

Commands
========

From the root directory of your project you have the following sub-commands available:

You can combine the commands together like ``clickable build click-build install launch``

``clickable``
-------------

Runs the default sub-commands specified in the "default" config. A dirty build
without cleaning the build dir can be achieved by running
``clickable --dirty``.

``clickable desktop``
---------------------

Compile and run the app on the desktop.

Note: ArchLinux user might need to run ``xhost +local:clickable`` before using
desktop mode.

Run
``clickable desktop --debug``

to show the executed docker command.

``clickable create``
--------------------

Generate a new app from a list of :ref:`app template options <app-templates>`.

``clickable create <app template name>``

Generate a new app from an :ref:`app template <app-templates>` by name.

``clickable shell``
-------------------

Opens a shell on the device via ssh. This is similar to the ``phablet-shell`` command.

``clickable clean-libs``
------------------------

Cleans out all library build dirs.

``clickable build-libs``
------------------------

Builds the dependency libraries specified in the clickable.json.

``clickable clean``
-------------------

Cleans out the build dir.

``clickable build``
-------------------

Builds the project using the specified template, build dir, and build commands.

``clickable click-build``
-------------------------

Takes the built files and compiles them into a click package (you can find it in the build dir).

``clickable click-build --output=/path/to/some/diretory``

Takes the built files and compiles them into a click package, outputting the
compiled click to the directory specified by ``--output``.

``clickable review``
--------------------

Takes the built click package and runs click-review against it. This allows you
to review your click without installing click-review on your computer.

.. _commands-test:

``clickable test``
--------------------

Run your test suite in with a virtual screen. By default this runs qmltestrunner,
but you can specify a custom command by setting the :ref:`test <clickable-json-test>`
property in your clickable.json.

``clickable install``
---------------------

Takes a built click package and installs it on a device.

``clickable install ./path/to/click/app.click``

Installs the specified click package on the device

``clickable launch``
--------------------

Launches the app on a device.

``clickable launch <app name>``

Launches the specified app on a device.

``clickable logs``
------------------

Follow the apps log file on the device.

``clickable log``
------------------

Dumps the apps log file on the device.

``clickable publish``
---------------------

Publish your click app to the OpenStore. Check the
:ref:`Getting started doc <getting-started>` for more info.

``clickable publish "changelog message"``

Publish your click app to the OpenStore with a message to add to the changelog.

``clickable run "some command"``
--------------------------------

Runs an arbitrary command in the clickable container.

``clickable update``
---------------------------

Update the docker container for use with clickable.

``clickable no-lock``
---------------------

Turns off the device's display timeout.

``clickable writable-image``
----------------------------

Make your Ubuntu Touch device's rootfs writable. This replaces to old
``phablet-config writable-image`` command.

``clickable devices``
---------------------

Lists the serial numbers and model names for attached devices. Useful when
multiple devices are attached and you need to know what to use for the ``-s``
argument.

``clickable <custom command>``
------------------------------

Runs a custom command specified in the "scripts" config

.. _container-mode:

``clickable <any command> --container-mode``
--------------------------------------------

Runs all builds commands on the current machine and not in a container. This is
useful from running clickable from within a container.

.. _nvidia:

``clickable desktop --nvidia``
------------------------------

``clickable`` checks automatically if nvidia-drivers are installed and turns on nvidia mode.
The ``--nvidia`` flag lets you manually enforce nvidia mode.

Depending on your docker version, the docker execution will change and
you need to provide additional system requirements:

**docker &lt; 19.03 system requirements**

* nvidia-modprobe
* nvidia-docker

On Ubuntu, install these requirements using ``apt install nvidia-modprobe nvidia-docker``.

**docker &gt;= 19.03 system requirements**

* nvidia-container-toolkit

On Ubuntu, install these requirements using ``apt install nvidia-container-toolkit``.

Run clickable with the ``--debug`` flag to see the executed command for your system.
