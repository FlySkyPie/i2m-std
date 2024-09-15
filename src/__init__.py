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
from bpy.props import (
    PointerProperty,
)

from .clearslot import KeI2Mclearslot
from .batchbrowser import KeI2Mbatchbrowser
from .filebrowser import KeI2Mfilebrowser
from .reload import KeI2Mreload
from .main import KeI2M
from .ui import VIEW3D_PT_i2m
from .prefs.addonprefs import KeI2Maddonprefs
from .prefs.props import KeI2Mprops

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
