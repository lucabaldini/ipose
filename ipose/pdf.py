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

"""Tools for operating on pdf files.
"""

import pathlib

import PIL.Image
import pypdfium2

from ipose import logger
from ipose.utils import check_input_file


def open_document(file_path: str | pathlib.Path) -> pypdfium2._helpers.document.PdfDocument:
    """Open a pdf document.
    """
    check_input_file(file_path, '.pdf')
    logger.info(f'Opening input pdf document {file_path}...')
    document = pypdfium2.PdfDocument(file_path)
    logger.info(f'Done, document has {len(document)} page(s).')
    return document


def rasterize(file_path: str | pathlib.Path, page_number: int = 0,
    output_width: int = 5000) -> PIL.Image.Image:
    """Rasterize a single page of a pdf document into a ``PIL.Image.Image`` object.

    Parameters
    ----------
    file_path
        The path to the input pdf document.

    page_number
        The target page number.
    """
    document = open_document(file_path)
    logger.info(f'Rastering page {page_number}...')
    page = document.get_page(page_number)
    # Retrieve the page size in canvas units (1/72 inch)
    original_width, original_height = page.get_size()
    aspect_ratio = original_height / original_width
    logger.debug(f'Original page size: {original_width:.3f} x {original_height:.3f} '
        f'aspect ratio = {aspect_ratio:.3f}')
    kwargs = dict(scale=output_width / original_width)
    logger.debug(f'Rendering options: {kwargs}')
    image = page.render(**kwargs).to_pil()
    return image



if __name__ == '__main__':
    from ipose import IPOSE_TEST_DATA
    file_path = IPOSE_TEST_DATA / 'sample_poster.pdf'
    image = rasterize(file_path)
    image.show()
