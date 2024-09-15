import bpy
from bpy.types import PropertyGroup, Operator, Panel, AddonPreferences
from bpy_extras.io_utils import ImportHelper

from .utilities import load_slot


class KeI2Mbatchbrowser(Operator, ImportHelper):
    bl_idname = "ke.i2m_batchbrowser"
    bl_label = "Batch Process Folder"
    bl_description = "Pick a folder to batch kei2m on ALL the images in the folder.\n --> Using last used settings <--"

    filter_glob: bpy.props.StringProperty(subtype="DIR_PATH")

    def execute(self, context):
        if not self.filepath:
            return {"CANCELLED"}

        # Load images in folder to Batch
        filter_glob = (
            ".png",
            ".tif",
            ".tiff",
            ".exr",
            ".hdr",
            ".tga",
            ".sgi",
            ".rgb",
            ".bw",
            ".jp2",
            ".j2c",
            ".cin",
            ".dpx",
        )
        images = []
        img_count = 0

        for file in os.listdir(self.filepath):
            if file.lower().endswith(filter_glob):
                path = os.path.join(self.filepath, file)
                img = load_slot(path)
                if img is not None:
                    img_count += 1
                    images.append(file)

        if not images:
            sys.stdout.write(
                "\nkei2m Batch Process Aborted: No images could be loaded\n"
            )
            self.report({"INFO"}, "Aborted: No images could be loaded")
            return {"CANCELLED"}

        sys.stdout.write("\nkei2m Batch Process Images Loaded: %s\n" % str(img_count))

        # Batch all loaded images
        k = context.scene.kei2m
        bpy.ops.ke.i2m_clearslot(axis="ALL")

        for img in images:
            k.FRONT = img
            bpy.ops.ke.i2m(batch=True)

        k.FRONT = ""
        return {"FINISHED"}
