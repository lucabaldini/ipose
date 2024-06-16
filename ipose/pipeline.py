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

from ipose import logger, IPOSE_DATA
from ipose.raster import Rectangle, run_face_recognition, open_image, resize_image,\
    elliptical_mask, save_image


def _filter_kwargs(*keys, **kwargs):
    """
    """
    return {key: value for key, value in kwargs.items() if key in keys}


def ipose_face_crop(file_path: str | pathlib.Path, **kwargs) -> None:
    """
    """
    if not isinstance(file_path, pathlib.Path):
        file_path = pathlib.Path(file_path)
    _kwargs = _filter_kwargs('scale_factor', 'min_neighbors', 'min_size')
    candidates = run_face_recognition(file_path, **_kwargs)
    num_candidates = len(candidates)
    image = open_image(file_path)
    if num_candidates == 0:
         logger.warning(f'No face candidate found in {file_path}, taking largest square...')
         candidates.append(Rectangle.square_from_image(image))
    if num_candidates > 1:
         logger.warning(f'Multiple face candidates found in {file_path}, taking largest...')
    # Go on with the best face candidate. Note that we cache the rectangles at all
    # the intermediate steps for debugging purposes, in case we need them...
    rect = candidates[-1]
    _kwargs = _filter_kwargs('horizontal_padding', 'top-scale-factor')
    pad_rect = rect.pad_face(**_kwargs)
    fit_rect = pad_rect.fit_to_image(image)
    # if interactive:
    #     # This is tricky, as the stuff we draw seems to be sticking around
    #     # even after the resize, which supposidly is making a copy...
    #     logger.debug(f'Original bounding box: {rect.bounding_box()}')
    #     logger.debug(f'Padded bounding box: {pad_rect.bounding_box()}')
    #     draw = PIL.ImageDraw.Draw(image)
    #     draw.rectangle(rect.bounding_box(), outline='white', width=2)
    #     draw.rectangle(pad_rect.bounding_box(), outline='yellow', width=2)
    #     draw.rectangle(fit_rect.bounding_box(), outline='red', width=2)
    #     image.show()
    box = fit_rect.bounding_box()
    logger.info(f'Target face bounding box: {box}')
    size = kwargs['output_size']
    image = resize_image(image, size, size, box=box)
    if kwargs['circular_mask']:
         image.putalpha(elliptical_mask(image))
    file_name = file_path.stem
    suffix = kwargs['suffix']
    if suffix is not None:
        file_name = f'{file_name}_{suffix}'
    file_name = f'{file_name}.png'
    save_image(image, IPOSE_DATA / file_name)
