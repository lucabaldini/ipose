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


from PySide6 import QtCore, QtGui, QtWidgets


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

    debug
        Debug flag. If True,
    """

    def __init__(self, parent: QtWidgets.QWidget=None, debug: bool = False) -> None:
        """Constructor.
        """
        super().__init__(parent)
        self.setLayout(QtWidgets.QGridLayout())
        self._debug = debug

    def add_widget(self, widget: QtWidgets.QWidget, row: int, column: int,
        row_span: int = 1, column_span: int = 1) -> QtWidgets.QWidget:
        """Add a widget to the underlying QGridLayout object.
        """
        if self._debug:
            widget.setStyleSheet("border: 1px solid black;")
        self.layout().addWidget(widget, row, column, row_span, column_span)
        return widget

    def add_text_label(self, row: int, column: int, row_span: int = 1,
        column_span: int = 1, text: str = None, font_size: int = None) -> QtWidgets.QLabel:
        """Add a text label to the underlying QGridLayout object.
        """
        label = QtWidgets.QLabel()
        font = label.font()
        if font_size is not None:
            font.setPointSize(font_size)
            label.setFont(font)
        if text is not None:
            label.setText(text)
        return self.add_widget(label, row, column, row_span, column_span)



class Header(LayoutWidget):

    """The screen header.
    """

    def __init__(self, title: str, subtitle: str = None, parent: QtWidgets.QWidget=None,
        debug: bool = False, **kwargs):
        """Constructor.
        """
        title_font_size = kwargs.get('title_font_size', 20)
        subtitle_font_size = kwargs.get('subtitle_font_size', 18)
        super().__init__(parent, debug)
        self.title_label = self.add_text_label(0, 0, text=title, font_size=title_font_size)
        self.subtitle_label = self.add_text_label(1, 0, text=subtitle, font_size=subtitle_font_size)

    def set_title(self, text):
        """Set the subtitle.
        """
        self.title_label.setText(text)

    def set_subtitle(self, text):
        """Set the subtitle.
        """
        self.subtitle_label.setText(text)




class PosterBanner:

    """A banner encapsulating all the poster information (presenter, title, qr code
    and alike).
    """



class Footer:

    """The screen footer.
    """



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    header = Header('Title', 'A very, very long subtitle', debug=True)
    header.show()
    sys.exit(app.exec())
