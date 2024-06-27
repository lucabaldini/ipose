# Copyright (C) 2024 the ipose team.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Graphical user interface.
"""

import pathlib

import ipose.config
from ipose.__qt__ import QtCore, QtGui, QtWidgets



class Canvas(QtWidgets.QLabel):

    """
    """

    def __init__(self, parent: QtWidgets.QWidget = None, size: tuple[int, int] = None) -> None:
        """Constructor.
        """
        super().__init__(parent)
        if size is not None:
            self.setFixedSize(*size)

    def paint(self, source: str | pathlib.Path | QtGui.QPixmap) -> None:
        """
        """
        if not isinstance(source, QtGui.QPixmap):
            source = QtGui.QPixmap(f'{source}')
        self.setPixmap(source)



class LayoutWidget(QtWidgets.QWidget):

    """Base class for all the GUI widgets.

    This is supposed to act as a base class for all the widgets in the graphical
    user interface, and encapsulates some useful methods that can then easily
    reused downstream.

    Any LayoutWidget object comes equipped with a QGridLayout that can be used to
    add other widgets.

    Parameters
    ----------
    parent
        The parent widget.
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        super().__init__(parent)
        self.setLayout(QtWidgets.QGridLayout())

    def add_widget(self, widget: QtWidgets.QWidget, row: int, column: int,
        row_span: int = 1, column_span: int = 1) -> QtWidgets.QWidget:
        """Add a widget to the underlying QGridLayout object.
        """
        if ipose.config.get('gui.debug') and isinstance(widget, QtWidgets.QLabel):
            widget.setStyleSheet("border: 1px solid black;")
        self.layout().addWidget(widget, row, column, row_span, column_span)
        return widget

    def add_canvas(self, row: int, column: int, row_span: int = 1, column_span: int = 1,
        size: tuple[int, int] = None) -> QtWidgets.QLabel:
        """Add a picture label to the underlying QGridLayout object.
        """
        canvas = Canvas(self, size)
        return self.add_widget(canvas, row, column, row_span, column_span)

    def add_text_label(self, row: int, column: int, row_span: int = 1,
        column_span: int = 1, font_size: int = None) -> QtWidgets.QLabel:
        """Add a text label to the underlying QGridLayout object.
        """
        label = QtWidgets.QLabel()
        font = label.font()
        if font_size is not None:
            font.setPointSize(font_size)
            label.setFont(font)
        return self.add_widget(label, row, column, row_span, column_span)



class Header(LayoutWidget):

    """The screen header.
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        height = ipose.config.get('gui.header.height')
        title_size = ipose.config.get('gui.header.title_size')
        subtitle_size = ipose.config.get('gui.header.subtitle_size')
        super().__init__(parent)
        self.title_label = self.add_text_label(0, 0, font_size=title_size)
        self.subtitle_label = self.add_text_label(1, 0, font_size=subtitle_size)
        self.setFixedHeight(height)

    def set_title(self, text: str) -> None:
        """Set the subtitle.
        """
        self.title_label.setText(text)

    def set_subtitle(self, text: str) -> None:
        """Set the subtitle.
        """
        self.subtitle_label.setText(text)



class RosterTable(LayoutWidget):

    """
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        #height = 200
        super().__init__(parent)
        #self.setFixedHeight(height)



class PosterBanner(LayoutWidget):

    """A banner encapsulating all the poster information (presenter, title, qr code
    and alike).
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        height = ipose.config.get('gui.banner.height')
        size = ipose.config.get('gui.banner.pic_size')
        super().__init__(parent)
        self.portrait_canvas = self.add_canvas(0, 0, size=size)
        self.qrcode_canvas = self.add_canvas(0, 1, size=size)
        self.roster_table = self.add_widget(RosterTable(self), 0, 2)
        self.presenter_label = self.add_text_label(1, 0, 1, 2)
        self.status_label = self.add_text_label(1, 2)
        self.setFixedHeight(height)

    def set_portrait(self, source: str | pathlib.Path | QtGui.QPixmap) -> None:
        """
        """
        self.portrait_canvas.paint(source)

    def set_qrcode(self, source: str | pathlib.Path | QtGui.QPixmap) -> None:
        """
        """
        self.qrcode_canvas.paint(source)



class PosterCanvas(LayoutWidget):

    """
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        width = ipose.config.get('gui.poster.width')
        super().__init__(parent)
        self.poster_label = self.add_canvas(0, 0)
        self.layout().setColumnMinimumWidth(0, width)



class Footer(LayoutWidget):

    """The screen footer.
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        height = ipose.config.get('gui.footer.height')
        message_size = ipose.config.get('gui.footer.message_size')
        super().__init__(parent)
        self.setFixedHeight(height)
        self.message_label = self.add_text_label(0, 0, font_size=message_size)

    def set_message(self, text: str) -> None:
        """Set the subtitle.
        """
        self.message_label.setText(text)



class DisplayWindow(LayoutWidget):

    """
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        super().__init__(parent)
        self.header = self.add_widget(Header(self), 0, 0)
        self.banner = self.add_widget(PosterBanner(self), 1, 0)
        self.canvas = self.add_widget(PosterCanvas(self), 2, 0)
        self.layout().setRowStretch(2, 1)
        self.footer = self.add_widget(Footer(self), 3, 0)



if __name__ == '__main__':
    import sys
    from ipose import IPOSE_TEST_DATA
    from ipose.__qt__ import exec_qapp
    app = QtWidgets.QApplication(sys.argv)
    ipose.config.set('gui.debug', True)
    window = DisplayWindow()
    window.header.set_title('An awesome conference')
    window.header.set_subtitle('With a very, very long subtitle')
    window.footer.set_message('And this is a debug message...')
    window.banner.set_portrait(IPOSE_TEST_DATA / 'mona_lisa_crop.png')
    window.banner.presenter_label.setText('A. Student')
    window.banner.status_label.setText('Status message')
    window.show()
    exec_qapp(app)
