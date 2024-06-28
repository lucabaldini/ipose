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

"""Package logo.
"""

from matplotlib import pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as patches

from ipose import IPOSE_DATA


VERTS = [(0.2, 0.0),
         (0.8, 0.0), # start of the lower right corner
         (1.0, 0.0), # intermediate point (as if it wasn't rounded)
         (1.0, 0.2), # end point of the lower right corner
         (1.0, 0.8), # move to the next point etc.
         (1.0, 1.0),
         (0.8, 1.0),
         (0.2, 1.0),
         (0.0, 1.0),
         (0.0, 0.8),
         (0.0, 0.2),
         (0.0, 0.0),
         (0.2, 0.0)]

CODES = [mpath.Path.MOVETO,
         mpath.Path.LINETO,
         mpath.Path.CURVE3,
         mpath.Path.CURVE3,
         mpath.Path.LINETO,
         mpath.Path.CURVE3,
         mpath.Path.CURVE3,
         mpath.Path.LINETO,
         mpath.Path.CURVE3,
         mpath.Path.CURVE3,
         mpath.Path.LINETO,
         mpath.Path.CURVE3,
         mpath.Path.CURVE3]


def draw_logo(pad: float = 0.05, line_width: float = 16., line_color: str = 'black'):
    """Draw the glorious package logo.
    """
    path = mpath.Path(VERTS, CODES)
    plt.figure(f'ipose logo_{line_color}', figsize=(5, 5))
    plt.gca().set_aspect('equal')
    plt.gca().set_xlim(-pad, 1. + pad)
    plt.gca().set_ylim(-pad, 1. + pad)
    plt.gca().axis('off')
    plt.tight_layout(pad=1.025)
    patch = patches.PathPatch(path, facecolor='orange', lw=line_width, edgecolor=line_color)
    plt.gca().add_patch(patch)
    plt.plot((0.01, 0.4, 0.75, 0.99), (0.2, 0.8, 0.4, 0.6), lw=line_width, color=line_color)
    circle = patches.Circle((0.76, 0.76), 0.175, color=line_color)
    plt.gca().add_patch(circle)
    plt.text(0.5, 0.1, 'iPose', size=90, ha='center', color=line_color)



if __name__ == '__main__':
    for color in ('black', 'white'):
        draw_logo(line_color=color)
        plt.savefig(IPOSE_DATA / f'ipose_logo_{color}.png', transparent=True)
    plt.show()
