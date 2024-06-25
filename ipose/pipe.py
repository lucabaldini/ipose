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

import PIL.Image, PIL.ImageDraw

from ipose import logger
import ipose.opts
import ipose.pdf
import ipose.raster


def _filter_kwargs(*keys: str, **kwargs) -> dict:
    """Small convenience function for filtering keywors arguments and dispatching
    them to different function calls.

    This essenstially returns a copy of the input dictionary only containing the subset
    of keys specified as arguments.

    Parameters
    ----------
    keys
        The desired keys.

    kwargs
        The complete dictionary of keyword arguments.

    Returns
    -------
    dict
        A filtered dict of keyword arguments.
    """
    return {key: value for key, value in kwargs.items() if key in keys}


def _check_kwargs(valid_keys: tuple[str], **kwargs) -> None:
    """Make sure that the input keyword argument dictionary only contains keys in
    the predefined tuple passed as the first argument.

    This is raising a ``RuntimeError`` if any extraneous key is found.

    Parameters
    ----------
    valid_keys
        The tuple or list of vali keys.

    kwargs
        The complete dictionary of keyword arguments.
    """
    for key in kwargs:
        if key not in valid_keys:
            raise RuntimeError(f'Invalid keyword argument \'{key}\' (valid keys are {valid_keys})')


def _process_kwargs(valid_keys: tuple[str], **kwargs) -> dict:
    """Return the full set of option for a specific pipeline task call.

    This is basically doing three distinct things:

    * check that all the keyword arguments make sense for the specific task at hand;
    * retrieve all the default options from the :mod:`ipose.ops` modules;
    * update the default options with the actual keyword arguments being passed to
      the relevant function call.

    This is typically the first step of any pipeline call, and ensure that we always
    start with a complete and valid set of options that are reproducible across
    different applications.

    Parameters
    ----------
    valid_keys
        The tuple or list of vali keys.

    kwargs
        The complete dictionary of keyword arguments.

    Returns
    -------
    dict
        The updated dict of keyword arguments.
    """
    _check_kwargs(valid_keys, **kwargs)
    options = ipose.opts.default_kwargs(*valid_keys)
    options.update(**kwargs)
    return options


def _output_file_path(file_path: str | pathlib.Path, **kwargs) -> pathlib.Path:
    """Return the path to the output file, given that of the input file, for batch
    processing.

    This is basically starting from the stem of the input file path, adding the
    optional suffix if defined, changing the file extension and redirecting the
    thing to the output folder. Note that, being purely a convenient function to
    be used within this module, is driven by keyword arguments in order to make
    function call immediate; the keys we expect are ``output_folder``, ``file_type``,
    and ``suffix``.

    A ``RuntimeError`` is raised if the path to the output file is the same to that
    to the input file.

    Parameters
    ----------
    file_path
        The path to the input file.

    kwargs:
        The keyword arguments controlling the path manipulation (``output_folder``,
        ``file_type``, and ``suffix``).

    Returns
    -------
    pathlib.Path
        The path to the output file.
    """
    output_folder, file_type, suffix = [kwargs[key] for key in \
        ('output_folder', 'file_type', 'suffix')]
    file_name = pathlib.Path(file_path).stem
    if suffix is not None:
        file_name = f'{file_name}_{suffix}'
    file_name = f'{file_name}{file_type}'
    return pathlib.Path(output_folder) / file_name


#: Valid keyword arguments for the :meth:`rasterize` method.
RASTERIZE_VALID_KWARGS = ('page_number', 'intermediate_width', 'output_width',
    'output_folder', 'file_type', 'suffix', 'overwrite', 'interactive')

def rasterize(file_path: str | pathlib.Path, **kwargs) -> None:
    """Rasterize a single page of a given pdf document.
    """
    options = _process_kwargs(RASTERIZE_VALID_KWARGS, **kwargs)
    _opts = _filter_kwargs('page_number', **options)
    _opts['image_width'] = options['intermediate_width']
    image = ipose.pdf.rasterize(file_path, **_opts)
    image = ipose.raster.resize_image(image, width=options.get('output_width'))
    ipose.raster.save_image(image, _output_file_path(file_path, **options))


#: Valid keyword arguments for the :meth:`face_crop` method.
FACE_CROP_VALID_KWARGS = ('scale_factor', 'min_neighbors', 'min_size', 'horizontal_padding',
    'top_scale_factor', 'output_size', 'circular_mask', 'output_folder', 'file_type',
    'suffix', 'overwrite', 'interactive')

def face_crop(file_path: str | pathlib.Path, **kwargs) -> None:
    """Crop an image to face.
    """
    options = _process_kwargs(FACE_CROP_VALID_KWARGS, **kwargs)
    _opts = _filter_kwargs('scale_factor', 'min_neighbors', 'min_size', **options)
    try:
        candidates = ipose.raster.run_face_recognition(file_path, **_opts)
    except RuntimeError as exception:
        logger.error(f'{exception}, giving up on this one...')
        return
    num_candidates = len(candidates)
    image = ipose.raster.open_image(file_path)
    if num_candidates == 0:
        logger.warning(f'No face candidate found in {file_path}, picking generic square...')
        candidates.append(ipose.raster.Rectangle.square_from_size(*image.size))
    if num_candidates > 1:
        logger.warning(f'Multiple face candidates found in {file_path}, picking largest...')
    # Go on with the best face candidate.
    _opts = _filter_kwargs('horizontal_padding', 'top-scale-factor', **options)
    original_rectangle = candidates[-1]
    final_rectangle = original_rectangle.setup_for_face_cropping(*image.size, **_opts)
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
    ipose.raster.save_image(image, _output_file_path(file_path, **options))


#: Valid keyword arguments for the :meth:`face_crop` method.
TILE_VALID_KWARGS = ('tile_width', 'tile_height', 'aspect_ratio', 'output_file',
    'overwrite', 'interactive')

def tile(*file_list: str | pathlib.Path, **kwargs):
     """
     """
     options = _process_kwargs(TILE_VALID_KWARGS, **kwargs)
     num_images = len(file_list)
     tile_width, tile_height = kwargs['tile_width'], kwargs['tile_height']
     tiling = ipose.raster.optimal_rectangular_tiling(num_images, tile_width, tile_height)
     image = PIL.Image.new('RGB', tiling.image_size)
     for i, file_path in enumerate(file_list):
         im = ipose.raster.open_image(file_path)
         im = ipose.raster.resize_image(im, tile_width, tile_height)
         image.paste(im, tiling.tiling_dict[i])
     image.show()


# def animate():
#     """
#     """
#     pass

if __name__ == '__main__':
    import glob
    file_list = glob.glob('/home/lbaldini/iposedata/*')
    tile(*file_list)
