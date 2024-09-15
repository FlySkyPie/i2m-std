from bpy.types import PropertyGroup
from bpy.props import (
    BoolProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    IntProperty,
)


class KeI2Mprops(PropertyGroup):
    FRONT: StringProperty(default="", name="Front Image", description="-Y Axis Image")
    RIGHT: StringProperty(default="", name="Right Image", description="+X Axis Image")
    TOP: StringProperty(default="", name="Top Image", description="+Z Axis Image")
    BACK: StringProperty(default="", name="Back Image", description="+Y Axis Image")
    LEFT: StringProperty(default="", name="Left Image", description="-X Axis Image")
    BOTTOM: StringProperty(default="", name="Bottom Image", description="-Z Axis Image")
    autofill: BoolProperty(
        name="Autofill",
        default=False,
        description="Auto-Fill other slots by suffixes when loading an image.\n "
        "Valid suffixes:\n"
        "_front, _right, _top\n"
        "_back,  _left,  _bottom",
    )
    info: BoolProperty(
        name="kei2m General Info",
        default=False,
        description="Load Alpha Images to convert into mesh (in Object Mode).\n"
        "A single image is required for PLANE & SCREW (& C2M) modes.\n"
        "2 or more images are required for BOOLEAN mode.\n"
        "Adjust result in Redo Panel.\n"
        "Non-alpha color option in Addon Preferences.\n"
        "See progress output in Console Window.",
    )
    opacity: IntProperty(default=95)
    workres: StringProperty(default="128")
    geo: EnumProperty(
        items=[
            ("PLANE", "Plane", "Converts into a Plane Mesh", "", 1),
            (
                "SCREW",
                "Screw",
                "A Screw Modifier revolves one side of a (symmetrical) image to a cylindrical shape",
                "",
                2,
            ),
            (
                "BOOLEAN",
                "Boolean",
                "Uses 2-3 images (front + right/top) to carve out a rough 3d shape using Intersect",
                "",
                3,
            ),
            (
                "C2M",
                "Color 2 Material",
                "Splits along color borders and assigns color materials on an mesh plane",
                "",
                4,
            ),
        ],
        name="Geo Type",
        default="PLANE",
        description="Which type of geo conversion to use",
    )
    screw_flip: BoolProperty(default=False)
    screw_xcomp: IntProperty(default=15)
    reduce: StringProperty(default="SIMPLE")
    shade_smooth: BoolProperty(default=True)
    front_only: BoolProperty(default=False)
    qnd_mat: BoolProperty(default=False)
    apply: BoolProperty(default=False)
    apply_none: BoolProperty(default=False)
    angle: FloatProperty(default=0.5)
    custom_workres: IntProperty(default=0)
    vcolor: BoolProperty(default=False)
