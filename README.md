# napari-hsafm-browser

[![License](https://img.shields.io/pypi/l/napari-hsafm-browser.svg?color=green)](https://github.com/psichen/napari-hsafm-browser/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-hsafm-browser.svg?color=green)](https://pypi.org/project/napari-hsafm-browser)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-hsafm-browser.svg?color=green)](https://python.org)
[![tests](https://github.com/psichen/napari-hsafm-browser/workflows/tests/badge.svg)](https://github.com/psichen/napari-hsafm-browser/actions)
[![codecov](https://codecov.io/gh/psichen/napari-hsafm-browser/branch/main/graph/badge.svg)](https://codecov.io/gh/psichen/napari-hsafm-browser)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-hsafm-browser)](https://napari-hub.org/plugins/napari-hsafm-browser)

napari plugin for viewing high-speed AFM movies

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

## Installation

After download the plugin code and change to the plugin directory `napari-hsafm-browser/`, you can install `napari-hsafm-browser` via the command:

        pip install -e .

## Usage

This plugin is used for reading and viewing high-speed AFM `.asd` files in vim style.

First, open the directory which contains `.asd` files as the work directory. All `.asd` files in the work directory will be listed.

When one of the `.asd` files is selected, the corresponding movie will show up in the viewer window and the meta data will show up in the side bar.

The movie or frame will be saved in `tiff` format in the directory named by the value of `save to` when the key `y` or `<Shift-z>` are pressed. If no name is provided, the default directory name `imagej-tiff` will be used.

### key map

`j`: move to the next .asd file

`k`: move to the previous .asd file

`l`: step one slice of the movie forward

`h`: step one slice of the movie backward

`w`: step 10% slices of the movie forward

`b`: step 10% slices of the movie backward

`d`: move to the next 25% .asd file

`u`: move to the previous 25% .asd file

`^`: go to the begining of the movie

`$`: go to the end of the movie

`<Space>`: toggle play

`]`: double the fps (max: 160)

`[`: half the fps (min: 10)

`y`: save the current frame of the movie into a tiff file

`<Shift-z>`: copy the current .asd file to `save_dir`

`<Alt-c>`: reset contrast limit according to the current frame

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-hsafm-browser" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/psichen/napari-hsafm-browser/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/

## To do ##

1. fix height data in wide scanning.
2. continuous autoscale of contrast
3. continuous `h` and `l` keybinding functions.

