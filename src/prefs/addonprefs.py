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

from ..ui import VIEW3D_PT_i2m

# Panels to update
panels = (VIEW3D_PT_i2m,)


def update_panel(self, context):
    message = "kei2m : panel update failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = context.preferences.addons[
                "ke_i2m"
            ].preferences.category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format("ke_i2m", message, e))
        pass


class KeI2Maddonprefs(AddonPreferences):
    bl_idname = "ke_i2m"

    category: StringProperty(
        name="Tab Category",
        description="Choose a name (category) for tab placement",
        default="kei2m",
        update=update_panel,
    )
    use_rgb: BoolProperty(
        name="Use RGB instead of Alpha",
        default=False,
        description="Use the user RGB color instead of Alpha channel",
    )
    user_rgb: FloatVectorProperty(
        name="User RGB", subtype="COLOR", size=3, default=(1.0, 1.0, 1.0)
    )
    cap: IntProperty(
        default=16,
        name="Material Cap",
        description="Maximum number of materials generated in Color 2 Material Mode.",
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Tab Location (Category):")
        row.prop(self, "category", text="")
        row = layout.row(align=True)
        row.prop(self, "use_rgb", toggle=True)
        row.prop(self, "user_rgb", text="")
        row = layout.row()
        row.use_property_split = True
        row.prop(self, "cap")
