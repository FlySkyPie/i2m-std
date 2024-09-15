# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import bmesh
from bpy.types import PropertyGroup, Operator, Panel, AddonPreferences
from mathutils import Vector, Matrix
from bpy_extras.io_utils import ImportHelper
from collections import Counter
from bpy.props import (
    BoolProperty,
    PointerProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    IntProperty,
    FloatVectorProperty,
)

from .clearslot import KeI2Mclearslot
from .batchbrowser import KeI2Mbatchbrowser
from .filebrowser import KeI2Mfilebrowser
from .reload import KeI2Mreload
from .main import KeI2M
from .ui import VIEW3D_PT_i2m
from .prefs.addonprefs import KeI2Maddonprefs
from .prefs.props import KeI2Mprops

from .utilities import load_slot

bl_info = {
    "name": "kei2m",
    "author": "Kjell Emanuelsson",
    "category": "Import-Export",
    "version": (1, 3, 0, 7),
    "blender": (2, 80, 0),
    "location": "Viewport / N-Panel / kei2m",
    "warning": "",
    "description": "Image(s) To Mesh Generator",
    "doc_url": "https://ke-code.xyz",
}


def is_bversion(req_ver):
    """Is current Blender version the required version (as int: #### )"""
    if int("".join([str(i) for i in bpy.app.version]).ljust(4, "0")) < req_ver:
        return False
    return True


def make_entry(h, width, w, pixels):
    idx = (h * width) + w
    px_index = idx * 4
    return pixels[px_index : px_index + 4]


def alpha_check(images, rgb=False, c2m=False):
    has_alpha = True
    for img in images:
        if img.depth != 32 and not rgb and not c2m:
            has_alpha = False
    return has_alpha


def reduce_colors(pixelmap, threshold=0.51, cap=None):
    colors = [p[2] for p in pixelmap if p[2][3] == 1]
    color_groups = []
    common_colors = [c for c in Counter(colors).most_common()]
    if cap is not None:
        if len(common_colors) > cap:
            common_colors = common_colors[:cap]
    for c in common_colors:
        rmin = c[0][0] - threshold
        rmax = c[0][0] + threshold
        gmin = c[0][1] - threshold
        gmax = c[0][1] + threshold
        bmin = c[0][2] - threshold
        bmax = c[0][2] + threshold
        similar = [[c][0]]
        for oc in reversed(common_colors):
            if oc != c:
                if (
                    rmin < oc[0][0] < rmax
                    and gmin < oc[0][1] < gmax
                    and bmin < oc[0][2] < bmax
                ):
                    similar.append(oc[0])
                    common_colors.remove(oc)
        color_groups.append(similar)
    for p in pixelmap:
        for i, g in enumerate(color_groups):
            if p[2] in g:
                p[2] = g[0][0]
    return pixelmap, [g[0][0] for g in color_groups]


# ------------------------------------------------------------------------------------------------------------
# Registration
# ------------------------------------------------------------------------------------------------------------
classes = (
    KeI2M,
    VIEW3D_PT_i2m,
    KeI2Maddonprefs,
    KeI2Mprops,
    KeI2Mfilebrowser,
    KeI2Mreload,
    KeI2Mclearslot,
    KeI2Mbatchbrowser,
)


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.kei2m = PointerProperty(type=KeI2Mprops)

    # Force Panel Udpate, for custom tab location.
    try:
        if "bl_rna" in VIEW3D_PT_i2m.__dict__:
            bpy.utils.unregister_class(VIEW3D_PT_i2m)
        VIEW3D_PT_i2m.bl_category = bpy.context.preferences.addons[
            __name__
        ].preferences.category
        bpy.utils.register_class(VIEW3D_PT_i2m)
    except Exception as e:
        print("kei2m panel update failed:\n", e)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

    try:
        del bpy.types.Scene.kei2m

    except Exception as e:
        print("unregister fail:\n", e)


if __name__ == "__main__":
    register()
