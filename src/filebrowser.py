import os

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper
from bpy.props import (
    StringProperty,
)

from .utilities import load_slot, alpha_check


class KeI2Mfilebrowser(Operator, ImportHelper):
    bl_idname = "ke.i2m_filebrowser"
    bl_label = "Load Image(s)"
    bl_description = "Open filebrowser to load image(s)"

    filter_glob: StringProperty(
        default="*.png;*.tif;*.tiff;*.exr;*.hdr;*.tga;*.sgi;*.rgb;*.bw;*.jp2;*.j2c;*.cin;*.dpx",
        options={"HIDDEN"},
    )

    axis: StringProperty(name="Axis Name", default="", options={"HIDDEN"})

    def execute(self, context):
        print("\n[------------- keI2M Image Loader -------------]")
        k = context.scene.kei2m
        kap = context.preferences.addons["ke_i2m"].preferences

        loaded = bpy.path.basename(self.filepath).split(".")
        loaded_name = loaded[0]

        # filename check
        if len(loaded_name) > 63:
            print("Filename: '%s'" % loaded_name)
            print(
                "  -> Filename is too long (>64) - will be shortened (internally in Blender)\n"
                "  -> 'Reload Image(s)' operator will not work\n"
            )

        ext = "." + loaded[-1]
        loaded_dir = os.path.dirname(self.filepath)

        paths = [self.filepath]
        slots = [self.axis]

        if k.autofill and k.geo == "BOOLEAN":
            suffix = ["_front", "_right", "_top", "_back", "_left", "_bottom"]
            suffix_check = False

            if suffix[0] not in loaded_name:
                self.report(
                    {"INFO"},
                    "Failed to autoload %s - Wrong suffix for 1st slot" % loaded_name,
                )
                return {"CANCELLED"}

            for s in suffix:
                if s in loaded_name:
                    suffix_check = True
                    loaded_name = loaded_name.replace(s, "")
                    suffix.remove(s)
                    break
            if suffix_check:
                for s in suffix:
                    n = loaded_name + s + ext
                    f = os.path.join(loaded_dir, n)
                    paths.append(f)
                    su = s.upper()[1:]
                    slots.append(su)
            else:
                print("Autoload failed - Invalid suffix")

        alpha_missing = []
        c2m = True if k.geo == "C2M" else False

        for f, slot in zip(paths, slots):
            img = load_slot(f)
            if img is not None:
                filename = img.name
                k[slot] = filename
                context.area.tag_redraw()
                if filename:
                    if alpha_check([img], kap.use_rgb, c2m):
                        print("Image Loaded: %s" % filename)
                    else:
                        alpha_missing.append(filename)
                else:
                    self.report({"WARNING"}, "File Not Loaded")
        if alpha_missing:
            self.report({"WARNING"}, "Missing Alpha Channel: %s" % alpha_missing)

        return {"FINISHED"}
