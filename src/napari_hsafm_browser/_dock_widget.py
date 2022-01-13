import datetime
import re
from os import listdir, makedirs, path
import shutil

import tifffile
from magicgui.widgets import FileEdit
from napari.settings import SETTINGS
from napari_plugin_engine import napari_hook_implementation
from qtpy.QtWidgets import (
    QFileDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QWidget,
)

from hsafm_base.hsafm_base import HSAFM


class hsAFMBrowser(QWidget):
    def __init__(self, napari_viewer):
        super().__init__()
        self.viewer = napari_viewer
        file_list = QListWidget()
        meta_list = {
            "file_number": QLabel(),
            "scan_range": QLabel(),
            "pixels": QLabel(),
            "record_date": QLabel(),
            "record_time": QLabel(),
            "record_duration": QLabel(),
            "frame_time": QLabel(),
            "comment": QLabel(),
        }

        file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))

        self.setLayout(QVBoxLayout())
        dir_edit = FileEdit(value=file, mode="d")  # return one existing directory
        self.layout().addWidget(dir_edit.native)
        self.layout().addWidget(file_list)
        for key, value in meta_list.items():
            self.layout().addWidget(value)
        self.layout().addWidget(QLabel("save to"))
        save_to = QLineEdit()
        self.layout().addWidget(save_to)

        def dir_changed():
            self.current_dir = (
                str(dir_edit.value.absolute()).replace("\\", "/").replace("//", "/")
            )
            file_list.clear()
            for f in listdir(self.current_dir):
                if f.endswith(".asd"):
                    item = QListWidgetItem(f)
                    item.file_name = f
                    file_list.addItem(item)
            file_list.sortItems()
            file_list.setCurrentRow(0)

        def file_open():
            file = file_list.currentItem()
            if file:
                self.hsafm = HSAFM(path.join(self.current_dir, file.file_name))

            if self.viewer.window.qt_viewer.dims.is_playing:
                self.viewer.window.qt_viewer.dims.stop()

            if len(self.viewer.layers):
                for i in range(0, len(self.viewer.layers)):
                    self.viewer.layers.pop(i)
            self.viewer.add_image(
                self.hsafm.height,
                name="height (nm)",
                colormap=("afm-lut", self.hsafm.afm_lut),
            )

            self.viewer.window.qt_viewer.dims.slider_widgets[0].dims.set_current_step(
                0, 0
            )
            self.viewer.layers[0].reset_contrast_limits()
            SETTINGS.application.playback_fps = 10

            meta_list["scan_range"].setText(
                f"scan range (nm): \t {self.hsafm.xScanRange} x {self.hsafm.yScanRange}"
            )
            meta_list["pixels"].setText(
                f"pixels: \t\t {self.hsafm.xPixel} x {self.hsafm.yPixel}"
            )
            meta_list["record_date"].setText(
                f"record date: \t {datetime.date(self.hsafm.yearRec, self.hsafm.monthRec, self.hsafm.dayRec)}"
            )
            meta_list["record_time"].setText(
                f"record time: \t {datetime.time(self.hsafm.hourRec, self.hsafm.minuteRec, self.hsafm.secondRec)}"
            )
            meta_list["record_duration"].setText(
                f"record duration: \t {datetime.timedelta(milliseconds=self.hsafm.frameAcqTime*self.hsafm.frameNumber[-1])}"
            )
            meta_list["frame_time"].setText(
                f"frame time (s): \t {self.hsafm.frameAcqTime/1000}"
            )
            meta_list["comment"].setText(f"comment: \t\t {self.hsafm.comment}")

        @self.viewer.bind_key("Space")
        def toggle_play(viewer):
            if not viewer.window.qt_viewer.dims.is_playing:
                viewer.window.qt_viewer.dims.play()
            else:
                viewer.window.qt_viewer.dims.stop()

        @self.viewer.bind_key("j")
        def next_file(viewer):
            if file_list.currentRow() < file_list.count() - 1:
                file_list.setCurrentRow(file_list.currentRow() + 1)

        @self.viewer.bind_key("k")
        def prev_file(viewer):
            if file_list.currentRow() > 0:
                file_list.setCurrentRow(file_list.currentRow() - 1)

        @self.viewer.bind_key("l")
        def forward_one_step(viewer):
            _current = viewer.window.qt_viewer.dims.slider_widgets[0].dims.current_step[
                0
            ]
            _max = viewer.window.qt_viewer.dims.slider_widgets[0].dims.nsteps[0]
            _step = 1
            _forward = _current + _step
            _forward = _forward if _forward <= _max else _max
            viewer.window.qt_viewer.dims.slider_widgets[0].dims.set_current_step(
                0, _forward
            )

        @self.viewer.bind_key("h")
        def backward_one_step(viewer):
            _current = viewer.window.qt_viewer.dims.slider_widgets[0].dims.current_step[
                0
            ]
            _step = 1
            _backward = _current - _step
            _backward = _backward if _backward >= 0 else 0
            viewer.window.qt_viewer.dims.slider_widgets[0].dims.set_current_step(
                0, _backward
            )

        @self.viewer.bind_key("]")
        def speed_up(viewer):
            _fps = SETTINGS.application.playback_fps
            _fps *= 2
            if _fps > 160:
                SETTINGS.application.playback_fps = 160
            else:
                SETTINGS.application.playback_fps = _fps

        @self.viewer.bind_key("[")
        def slow_down(viewer):
            _fps = SETTINGS.application.playback_fps
            _fps /= 2
            if _fps < 5:
                SETTINGS.application.playback_fps = 5
            else:
                SETTINGS.application.playback_fps = _fps

        @self.viewer.bind_key("=")
        def reset_speed(viewer):
            SETTINGS.application.playback_fps = 10

        @self.viewer.bind_key("w")
        def forward_steps(viewer):
            _current = viewer.window.qt_viewer.dims.slider_widgets[0].dims.current_step[
                0
            ]
            _max = viewer.window.qt_viewer.dims.slider_widgets[0].dims.nsteps[0]
            _step = int(_max / 10) if int(_max / 10) else 1
            _forward = _current + _step
            _forward = _forward if _forward <= _max else _max
            viewer.window.qt_viewer.dims.slider_widgets[0].dims.set_current_step(
                0, _forward
            )

        @self.viewer.bind_key("b")
        def backward_steps(viewer):
            _current = viewer.window.qt_viewer.dims.slider_widgets[0].dims.current_step[
                0
            ]
            _max = viewer.window.qt_viewer.dims.slider_widgets[0].dims.nsteps[0]
            _step = int(_max / 10) if int(_max / 10) else 1
            _backward = _current - _step
            _backward = _backward if _backward >= 0 else 0
            viewer.window.qt_viewer.dims.slider_widgets[0].dims.set_current_step(
                0, _backward
            )

        @self.viewer.bind_key("d")
        def next_couple_files(viewer):
            if file_list.currentRow() < file_list.count() - 1:
                _step = int(file_list.count() / 4) if int(file_list.count() / 4) else 1
                file_list.setCurrentRow(file_list.currentRow() + _step) if file_list.currentRow() + _step < file_list.count()-1 else file_list.setCurrentRow(file_list.count()-1)

        @self.viewer.bind_key("u")
        def prev_couple_files(viewer):
            if file_list.currentRow() > 0:
                _step = int(file_list.count() / 4) if int(file_list.count() / 4) else 1
                file_list.setCurrentRow(file_list.currentRow() - _step) if file_list.currentRow() - _step > 0 else file_list.setCurrentRow(0)

        @self.viewer.bind_key("^")
        def go_first(viewer):
            viewer.window.qt_viewer.dims.slider_widgets[0].dims.set_current_step(0, 0)

        @self.viewer.bind_key("$")
        def go_end(viewer):
            _max = viewer.window.qt_viewer.dims.slider_widgets[0].dims.nsteps[0]
            viewer.window.qt_viewer.dims.slider_widgets[0].dims.set_current_step(
                0, _max
            )

        @self.viewer.bind_key("Alt-c")
        def reset_contrast(viewer):
            viewer.layers[0].reset_contrast_limits()

        @self.viewer.bind_key("Shift-z")
        def save_as_tiff(viewer):
            if save_to.text():
                save_dir = path.join(self.current_dir, save_to.text())
            else:
                save_dir = path.join(self.current_dir, "copied asd files")

            save_name = re.search(
                r"(.*).asd$", file_list.currentItem().file_name
            ).groups()[0]

            if not path.exists(save_dir):
                makedirs(save_dir)

            shutil.copy(path.join(self.current_dir, file_list.currentItem().file_name), save_dir)
            tifffile.imwrite(
                f"{save_dir}/{save_name}.tiff",
                viewer.layers["height (nm)"].data,
                imagej=True,
                resolution=(self.hsafm.xPixel/self.hsafm.xScanRange, self.hsafm.yPixel/self.hsafm.yScanRange),
                metadata={'axes':'TYX', 'unit':'nm', 'finterval':self.hsafm.frameAcqTime/1000},
            )

        @self.viewer.bind_key("y")
        def save_slice_as_tiff(viewer):
            if save_to.text():
                save_dir = path.join(self.current_dir, save_to.text())
            else:
                save_dir = path.join(self.current_dir, "imagej_tiff")

            current_slice = viewer.window.qt_viewer.dims.slider_widgets[
                0
            ].dims.current_step[0]
            save_name = re.search(
                r"(.*).asd$", file_list.currentItem().file_name
            ).groups()[0]

            if not path.exists(save_dir):
                makedirs(save_dir)

            tifffile.imwrite(
                f"{save_dir}/{save_name}-{current_slice}.tiff",
                viewer.layers["height (nm)"].data[current_slice],
                imagej=True,
            )

        dir_edit.line_edit.changed.connect(dir_changed)
        file_list.currentItemChanged.connect(file_open)
        dir_changed()  # run once to initialize


@napari_hook_implementation
def napari_experimental_provide_dock_widget():
    return [hsAFMBrowser]
