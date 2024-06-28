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

from ipose import IPOSE_QSS, logger
import ipose.config
from ipose.__qt__ import QtCore, QtGui, QtWidgets


_DEFAULT_STYLESHEET = IPOSE_QSS / 'default.qss'


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



class LayoutFrame(QtWidgets.QFrame):

    """Base class for all the GUI widgets.

    This is supposed to act as a base class for all the widgets in the graphical
    user interface, and encapsulates some useful methods that can then easily
    reused downstream.

    Any LayoutFrame object comes equipped with a QGridLayout that can be used to
    add other widgets.

    Parameters
    ----------
    parent
        The parent widget.
    """

    def __init__(self, parent: QtWidgets.QWidget = None, margins: int = 0) -> None:
        """Constructor.
        """
        super().__init__(parent)
        self.setLayout(QtWidgets.QGridLayout(self))
        self.layout().setContentsMargins(margins, margins, margins, margins)

    def add_widget(self, widget: QtWidgets.QWidget, row: int, column: int,
        row_span: int = 1, column_span: int = 1, object_name: str = None) -> QtWidgets.QWidget:
        """Add a widget to the underlying QGridLayout object.
        """
        if ipose.config.get('gui.debug'):
            widget.setStyleSheet("border: 1px solid black;")
        self.layout().addWidget(widget, row, column, row_span, column_span)
        if object_name is not None:
            widget.setObjectName(object_name)
        return widget

    def add_text_label(self, row: int, column: int, row_span: int = 1,
        column_span: int = 1, object_name: str = None) -> QtWidgets.QLabel:
        """Add a text label to the underlying QGridLayout object.
        """
        label = QtWidgets.QLabel(self)
        return self.add_widget(label, row, column, row_span, column_span, object_name)

    def add_canvas(self, row: int, column: int, row_span: int = 1, column_span: int = 1,
        size: tuple[int, int] = None, object_name: str = None) -> QtWidgets.QLabel:
        """Add a picture label to the underlying QGridLayout object.
        """
        canvas = Canvas(self, size)
        return self.add_widget(canvas, row, column, row_span, column_span, object_name)



class Header(LayoutFrame):

    """The screen header.
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        logo_size = ipose.config.get('gui.header.logo_size')
        super().__init__(parent)
        self.title_label = self.add_text_label(0, 0, object_name='title')
        self.subtitle_label = self.add_text_label(1, 0, object_name='subtitle')
        self.logo_canvas = self.add_canvas(0, 1, 3, size=logo_size, object_name='logo')

    def set_title(self, text: str) -> None:
        """Set the subtitle.
        """
        self.title_label.setText(text)

    def set_subtitle(self, text: str) -> None:
        """Set the subtitle.
        """
        self.subtitle_label.setText(text)

    def set_logo(self, file_path: str | pathlib.Path) -> None:
        """
        """
        self.logo_canvas.paint(file_path)



class RosterTable(LayoutFrame):

    """
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        #height = 200
        super().__init__(parent)
        #self.setFixedHeight(height)



class PosterBanner(LayoutFrame):

    """A banner encapsulating all the poster information (presenter, title, qr code
    and alike).
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        size = ipose.config.get('gui.banner.pic_size')
        super().__init__(parent)
        self.portrait_canvas = self.add_canvas(0, 0, size=size)
        self.qrcode_canvas = self.add_canvas(0, 1, size=size)
        self.roster_table = self.add_widget(RosterTable(self), 0, 2)
        self.name_label = self.add_text_label(1, 0, 1, 2, object_name='name')
        self.affiliation_label = self.add_text_label(2, 0, 1, 2, object_name='affiliation')
        self.status_label = self.add_text_label(2, 2, object_name='message')

    def set_portrait(self, source: str | pathlib.Path | QtGui.QPixmap) -> None:
        """
        """
        self.portrait_canvas.paint(source)

    def set_qrcode(self, source: str | pathlib.Path | QtGui.QPixmap) -> None:
        """
        """
        self.qrcode_canvas.paint(source)

    def set_presenter(self, name: str, affiliation: str) -> None:
        """
        """
        self.name_label.setText(name)
        self.affiliation_label.setText(affiliation)

    def set_status(self, text: str) -> None:
        """
        """
        self.status_label.setText(text)



class PosterCanvas(LayoutFrame):

    """
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        width = ipose.config.get('gui.poster.width')
        super().__init__(parent)
        self.poster_canvas = self.add_canvas(0, 0)
        self.layout().setColumnMinimumWidth(0, width)



class Footer(LayoutFrame):

    """The screen footer.
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        super().__init__(parent)
        self.message_label = self.add_text_label(0, 0, object_name='message')
        self.setFixedHeight(ipose.config.get('gui.footer.height'))

    def set_message(self, text: str) -> None:
        """Set the subtitle.
        """
        self.message_label.setText(text)



class DisplayWindow(LayoutFrame):

    """
    """

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        """Constructor.
        """
        super().__init__(parent)
        self.header = self.add_widget(Header(self), 0, 1, object_name='header')
        self.banner = self.add_widget(PosterBanner(self), 1, 1, object_name='banner')
        self.canvas = self.add_widget(PosterCanvas(self), 2, 1, object_name='canvas')
        self.footer = self.add_widget(Footer(self), 3, 1, object_name='footer')
        self.layout().setRowStretch(2, 1)
        self.layout().setColumnMinimumWidth(0, 10)
        self.layout().setColumnMinimumWidth(3, 10)
        self.layout().setColumnStretch(0, 1)
        self.layout().setColumnStretch(3, 1)


def bootstrap_qapplication() -> QtWidgets.QApplication:
    """Create a QApplication object and apply the proper stypesheet.
    """
    #pylint: disable=unspecified-encoding
    stylesheet = ipose.config.get('gui.stylesheet')
    if stylesheet is None:
        stylesheet = _DEFAULT_STYLESHEET
    qapp = QtWidgets.QApplication(sys.argv)
    logger.info(f'Applying stylesheet {stylesheet} to the main application...')
    with open(stylesheet, 'r') as stylesheet:
        qapp.setStyleSheet(stylesheet.read())
    return qapp



if __name__ == '__main__':
    import sys
    from ipose import IPOSE_TEST_DATA
    from ipose.__qt__ import exec_qapp
    app = bootstrap_qapplication()
    #print(QtGui.QFontDatabase.families())
    #ipose.config.set('gui.debug', True)
    window = DisplayWindow()
    window.header.set_title('First Topical Conference on Something Very Interesting')
    window.header.set_subtitle('Far, Far Away Land, Once Upon a time')
    window.footer.set_message('And this is a debug message...')
    window.banner.set_portrait(IPOSE_TEST_DATA / 'mona_lisa_crop.png')
    window.banner.set_qrcode(IPOSE_TEST_DATA / 'ipose_qrcode.png')
    window.banner.set_presenter('Monna Lisa', 'Gherardini Family (Florence)')
    window.canvas.poster_canvas.paint(IPOSE_TEST_DATA / 'leonardo.png')
    window.banner.set_status('Status messages will be displayed in this box...')
    window.show()
    exec_qapp(app)
