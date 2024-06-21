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

"""Pipeline facilities.
"""

import pathlib

import PIL.ImageDraw

from ipose import logger, IPOSE_DATA
import ipose.pdf
import ipose.raster


def _filter_kwargs(*keys, **kwargs):
    """Small convenience function for filtering keywors arguments and dispatching
    them to different function calls.

    Parameters
    ----------
    keys
        The desired keys.

    kwargs
        The complete dictionary of keyword arguments.

    Returns
    -------
        A filtered dict of keyword arguments.
    """
    return {key: value for key, value in kwargs.items() if key in keys}


def _output_file_path(file_path: str | pathlib.Path, file_extension: str, output_folder: str,
    suffix: str = None) -> str:
    """
    """
    file_name = pathlib.Path(file_path).stem
    if suffix is not None:
        file_name = f'{file_name}_{suffix}'
    file_name = f'{file_name}{file_extension}'
    return pathlib.Path(output_folder) / file_name


def face_crop(file_path: str | pathlib.Path, **kwargs) -> None:
    """
    """
    _kwargs = _filter_kwargs('scale_factor', 'min_neighbors', 'min_size', **kwargs)
    candidates = ipos.raster.run_face_recognition(file_path, **_kwargs)
    num_candidates = len(candidates)
    image = ipose.raster.open_image(file_path)
    if num_candidates == 0:
         logger.warning(f'No face candidate found in {file_path}, picking generic square...')
         candidates.append(ipose.raster.Rectangle.square_from_size(*image.size))
    if num_candidates > 1:
         logger.warning(f'Multiple face candidates found in {file_path}, picking largest...')
    # Go on with the best face candidate.
    _kwargs = _filter_kwargs('horizontal_padding', 'top-scale-factor', **kwargs)
    original_rectangle = candidates[-1]
    final_rectangle = original_rectangle.setup_for_face_cropping(*image.size, **_kwargs)
    if kwargs.get('interactive', False):
         draw = PIL.ImageDraw.Draw(image)
         draw.rectangle(original_rectangle.bounding_box(), outline='white', width=2)
         draw.rectangle(final_rectangle.bounding_box(), outline='red', width=2)
         image.show()
    box = final_rectangle.bounding_box()
    logger.info(f'Target face bounding box: {box}')
    size = kwargs.get('output_size', 100)
    image = ipose.raster.resize_image(image, size, size, box=box)
    if kwargs.get('circular_mask', False):
         image.putalpha(ipose.raster.elliptical_mask(image))
    file_name = pathlib.Path(file_path).stem
    suffix = kwargs.get('suffix')
    if suffix is not None:
        file_name = f'{file_name}_{suffix}'
    file_name = f'{file_name}.png'
    ipose.raster.save_image(image, pathlib.Path(kwargs.get('output_folder')) / file_name)


def rasterize(file_path: str | pathlib.Path, **kwargs) -> None:
    """
    """
    valid_kwargs = ('page_number', 'intermediate_width', 'output_width')
    _kwargs = _filter_kwargs(kwargs, 'page_number', 'output_width')
    image = ipose.pdf.rasterize(file_path, image_width=kwargs.get('intermediate_width'), **_kwargs)
    image = ipose.raster.resize_image(image, width=kwargs.get('output_width'))
    ipose.raster.save_image(image, _output_file_path(file_path, kwargs.get('file_type'),
        kwargs.get('output_folder'), kwargs.get('suffix')))


def tile():
    """
    """
    pass


def animate():
    """
    """
    pass
