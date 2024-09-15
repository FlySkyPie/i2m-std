from bpy.types import PropertyGroup, Operator, Panel, AddonPreferences
from bpy.props import (
    BoolProperty,
    PointerProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    IntProperty,
    FloatVectorProperty,
)


class KeI2Mclearslot(Operator):
    bl_idname = "ke.i2m_clearslot"
    bl_label = "Clear i2m File Slot"

    axis: StringProperty(name="Axis Name", default="")

    @classmethod
    def description(cls, context, properties):
        if properties.axis == "ALL":
            return "Clear All Image Slots"
        else:
            return "Clear Image Slot"

    def execute(self, context):
        k = context.scene.kei2m
        if self.axis == "ALL":
            for axis in ["FRONT", "RIGHT", "TOP", "BACK", "LEFT", "BOTTOM"]:
                k[axis] = ""
        else:
            k[self.axis] = ""
        context.area.tag_redraw()
        return {"FINISHED"}
